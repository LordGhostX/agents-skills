#!/usr/bin/env python3
"""Export public Codex rollout records and subagent sessions as readable text."""

import argparse
import json
import os
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import TextIO, TypeAlias, cast

JsonValue: TypeAlias = (
    None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
)
JsonObject: TypeAlias = dict[str, JsonValue]

MEDIA_TYPES = (
    "image",
    "input_image",
    "output_image",
    "audio",
    "input_audio",
    "output_audio",
)
ACTIVITY_FIELDS = {
    "SubAgentActivity": (
        "kind",
        "agent_thread_id",
        "agent_path",
        "model",
        "reasoning_effort",
    ),
    "CommandExecution": ("command", "cwd", "status", "exit_code", "aggregated_output"),
    "McpToolCall": ("server", "tool", "arguments", "status", "result"),
}


@dataclass(frozen=True)
class Record:
    timestamp: str
    kind: str
    payload: JsonObject


@dataclass(frozen=True)
class Session:
    path: Path
    id: str
    parent: str | None
    agent: str | None
    started_at: datetime


def decode_json(text: str) -> JsonValue:
    return cast(JsonValue, json.loads(text))


def parse_record(line: str) -> Record:
    value = decode_json(line)
    if not isinstance(value, dict):
        raise TypeError("Expected a JSON object")

    recorded_at = value.get("timestamp")
    kind = value.get("type")
    payload = value.get("payload")
    if (
        not isinstance(recorded_at, str)
        or not isinstance(kind, str)
        or not isinstance(payload, dict)
    ):
        raise TypeError("Expected timestamp/type strings and a payload object")

    return Record(recorded_at, kind, payload)


def optional_object(value: JsonValue) -> JsonObject:
    return value if isinstance(value, dict) else {}


def session_metadata(path: Path) -> Session | None:
    with path.open(encoding="utf-8") as log:
        first_line = log.readline()
    try:
        record = parse_record(first_line)
    except (json.JSONDecodeError, TypeError):
        return None
    if record.kind != "session_meta":
        return None

    payload = record.payload
    session_id = payload.get("id")
    if not isinstance(session_id, str):
        return None

    origin = optional_object(payload.get("source"))
    subagent = optional_object(origin.get("subagent"))
    spawn = optional_object(subagent.get("thread_spawn"))
    parent = payload.get("parent_thread_id") or spawn.get("parent_thread_id")
    agent = payload.get("agent_path") or spawn.get("agent_path")
    started_at = payload.get("timestamp") or record.timestamp
    if not isinstance(started_at, str):
        raise TypeError(f"Invalid session timestamp in {path}")

    return Session(
        path=path.resolve(),
        id=session_id,
        parent=parent if isinstance(parent, str) else None,
        agent=agent if isinstance(agent, str) else None,
        started_at=timestamp(started_at),
    )


def select_sessions(
    target: str, codex_home: Path, subagents: bool, until: datetime
) -> list[Session]:
    main = None
    target_path = Path(target).expanduser()
    if target_path.is_file():
        main = session_metadata(target_path)
        if main is None:
            raise ValueError(f"No Codex session metadata in {target_path}")
        if not subagents:
            return [main]

    sessions: list[Session] = []
    for directory in (codex_home / "sessions", codex_home / "archived_sessions"):
        for path in sorted(directory.rglob("*.jsonl")):
            metadata = session_metadata(path)
            if metadata is not None:
                sessions.append(metadata)

    if main is None:
        matches = [session for session in sessions if session.id == target]
        if len(matches) != 1:
            raise ValueError(
                f"Expected one session for {target!r}, found {len(matches)}; "
                "check --codex-home or pass the JSONL path"
            )
        main = matches[0]

    selected = [main]
    if not subagents:
        return selected

    children: dict[str, list[Session]] = {}
    for session in sessions:
        if session.parent and session.started_at <= until:
            children.setdefault(session.parent, []).append(session)

    seen = {main.id}
    for parent in selected:
        for child in children.get(parent.id, []):
            if child.id not in seen:
                selected.append(child)
                seen.add(child.id)
    return selected


def records(path: Path) -> Iterator[Record]:
    with path.open(encoding="utf-8") as log:
        for number, line in enumerate(log, 1):
            if not line.strip():
                continue
            try:
                record = parse_record(line)
            except json.JSONDecodeError as error:
                if not line.endswith("\n"):
                    print(
                        f"Skipped incomplete final record: {path}:{number}",
                        file=sys.stderr,
                    )
                    break
                raise ValueError(f"Invalid JSON at {path}:{number}") from error
            except TypeError as error:
                raise TypeError(
                    f"Invalid record at {path}:{number}: {error}"
                ) from error
            yield record


def redact_text(text: str, redactions: list[str]) -> str:
    for secret in redactions:
        text = text.replace(secret, "[REDACTED]")
    return text


def readable(value: JsonValue) -> JsonValue:
    if isinstance(value, str):
        if re.fullmatch(r"gAAAA[A-Za-z0-9_-]{93,}={0,2}", value):
            return "[Encrypted content unavailable]"
        if re.fullmatch(r"data:(?:image|audio)/[^\s,]+,\S*", value):
            return "[Binary media omitted]"
        return value
    if isinstance(value, list):
        return [readable(item) for item in value]
    if isinstance(value, dict):
        kind = value.get("type")
        if kind == "encrypted_content":
            return "[Encrypted content unavailable]"
        if (
            isinstance(kind, str)
            and kind in MEDIA_TYPES
            and any(
                key in value for key in ("data", "image_url", "audio", "input_audio")
            )
        ):
            return f"[{kind} omitted]"
        return {
            key: readable(item)
            for key, item in value.items()
            if key != "encrypted_content"
        }
    return value


def render(value: JsonValue, redactions: list[str]) -> str:
    cleaned = readable(value)
    if isinstance(cleaned, str):
        return cleaned

    # Match JSON string escaping without merging distinct redacted object keys.
    encoded_redactions = [
        json.dumps(secret, ensure_ascii=False)[1:-1] for secret in redactions
    ]
    return redact_text(
        json.dumps(cleaned, ensure_ascii=False, indent=2), encoded_redactions
    )


def render_content(content: JsonValue, redactions: list[str]) -> str:
    if not isinstance(content, list):
        return render(content, redactions)

    parts: list[str] = []
    for block in content:
        match block:
            case {"type": "text" | "input_text" | "output_text", "text": str(text)}:
                parts.append(text)
            case _:
                parts.append(render(block, redactions))
    return "\n".join(parts)


def public_entry(
    record: Record, nested: bool, redactions: list[str]
) -> tuple[str, str] | None:
    payload = record.payload
    match record.kind, payload.get("type"):
        case "response_item", "message":
            role = payload.get("role")
            phase = payload.get("phase")
            if (
                not isinstance(role, str)
                or role not in ("user", "assistant")
                or phase not in (None, "commentary", "partial_answer", "final_answer")
            ):
                return None
            label = role.upper() + (f" ({phase})" if phase else "")
            return label, render_content(payload.get("content", []), redactions)
        case "response_item", "agent_message":
            label = f"AGENT MESSAGE {payload.get('author', '?')} -> {payload.get('recipient', '?')}"
            return label, render_content(payload.get("content", []), redactions)
        case "response_item", "function_call" | "custom_tool_call":
            arguments = payload.get("arguments", payload.get("input", ""))
            if payload["type"] == "function_call" and isinstance(arguments, str):
                try:
                    arguments = decode_json(arguments)
                except json.JSONDecodeError:
                    pass
            names = [payload.get("namespace"), payload.get("name")]
            tool_name = ".".join(
                name for name in names if isinstance(name, str) and name
            )
            return f"TOOL CALL {tool_name} | {payload.get('call_id', '?')}", render(
                arguments, redactions
            )
        case "response_item", "function_call_output" | "custom_tool_call_output":
            return f"TOOL RESULT | {payload.get('call_id', '?')}", render_content(
                payload.get("output", ""), redactions
            )
        case "event_msg", "item_completed":
            item = optional_object(payload.get("item"))
            kind = item.get("type")
            if not isinstance(kind, str) or kind not in ACTIVITY_FIELDS:
                return None
            if kind != "SubAgentActivity" and not nested:
                return None
            selected = {key: item[key] for key in ACTIVITY_FIELDS[kind] if key in item}
            return kind, render(selected, redactions)
        case _:
            return None


def timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(
            "Timestamps must include a timezone, for example 2026-11-05T21:28:14Z"
        )
    return parsed.astimezone(UTC)


def export(
    sessions: list[Session],
    output: TextIO,
    until: datetime,
    nested: bool,
    redactions: list[str],
) -> int:
    def write(text: str) -> None:
        output.write(redact_text(text, redactions))

    write(
        f"CODEX TRANSCRIPT\nRoot session: {sessions[0].id}\nThrough: {until.isoformat()}\n\n"
        "Public messages, tool calls/results, and subagent activity in recorded session order.\n"
        "Private reasoning, system/developer instructions, and runtime metadata are excluded.\n"
        "Binary media and encrypted content use placeholders; existing truncation is preserved.\n"
        f"Nested command/connector records: {'included' if nested else 'omitted (may duplicate tool results)'}.\n"
    )
    total = 0
    for index, session in enumerate(sessions):
        session_label = (
            "MAIN SESSION" if index == 0 else f"SUBAGENT {session.agent or session.id}"
        )
        write(
            f"\n{'=' * 80}\n{session_label}\nSession: {session.id}\nSource: {session.path}\n{'=' * 80}\n"
        )
        count = 0
        for record in records(session.path):
            if timestamp(record.timestamp) > until:
                continue
            entry = public_entry(record, nested, redactions)
            if entry is not None:
                label, body = entry
                write(f"\n[{count:04d}] {record.timestamp} | {label}\n\n{body}\n")
                count += 1
        total += count
    return total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("session", help="Exact session ID or rollout JSONL path")
    parser.add_argument(
        "-o",
        "--output",
        required=True,
        type=Path,
        help="New transcript file; existing files are never overwritten",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", "~/.codex")),
        help="Codex data directory (default: CODEX_HOME or ~/.codex)",
    )
    parser.add_argument(
        "--until",
        type=timestamp,
        default=datetime.now(UTC),
        help="Inclusive ISO timestamp cutoff with timezone (default: export start)",
    )
    parser.add_argument(
        "--no-subagents", action="store_true", help="Export only the selected session"
    )
    parser.add_argument(
        "--include-nested-tools",
        action="store_true",
        help="Also include recorded command and connector details",
    )
    parser.add_argument(
        "--redact-file",
        type=Path,
        help="UTF-8 file with one literal value per line to replace with [REDACTED]",
    )
    return parser.parse_args()


def write_export(
    destination: Path,
    sessions: list[Session],
    until: datetime,
    nested: bool,
    redactions: list[str],
) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(
            descriptor, "w", encoding="utf-8", errors="backslashreplace"
        ) as output:
            return export(sessions, output, until, nested, redactions)
    except BaseException:
        destination.unlink()
        raise


def main() -> None:
    args = parse_args()
    destination = args.output.expanduser()
    try:
        sessions = select_sessions(
            args.session,
            args.codex_home.expanduser(),
            not args.no_subagents,
            args.until,
        )
        redactions = []
        if args.redact_file:
            values = (
                args.redact_file.expanduser()
                .read_text(encoding="utf-8-sig")
                .splitlines()
            )
            redactions = sorted(
                {value for value in values if value}, key=len, reverse=True
            )
        total = write_export(
            destination, sessions, args.until, args.include_nested_tools, redactions
        )
    except (OSError, ValueError, TypeError) as error:
        raise SystemExit(f"Error: {error}") from error
    print(f"Exported {total} entries from {len(sessions)} sessions to {destination}")


if __name__ == "__main__":
    main()
