#!/usr/bin/env python3
import argparse
import os
import shutil
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
source_root = repo_root / "skills"

# Files that only one agent understands. Other targets skip them.
CODEX_ONLY_FILES = {Path("agents") / "openai.yaml"}


def env_path(name):
    value = os.environ.get(name)
    return Path(value).expanduser() if value else None


def codex_root():
    home = env_path("CODEX_HOME") or Path.home() / ".codex"
    return env_path("CODEX_SKILLS_DIR") or home / "skills"


def claude_root():
    home = env_path("CLAUDE_CONFIG_DIR") or Path.home() / ".claude"
    return env_path("CLAUDE_SKILLS_DIR") or home / "skills"


def antigravity_root():
    default = Path.home() / ".gemini" / "config" / "skills"
    return env_path("ANTIGRAVITY_SKILLS_DIR") or default


TARGETS = {
    "codex": codex_root,
    "claude": claude_root,
    "antigravity": antigravity_root,
}


def parse_targets():
    parser = argparse.ArgumentParser(
        description="Install the skills in this repository for one or more agents."
    )
    parser.add_argument(
        "--target",
        action="append",
        choices=[*TARGETS, "all"],
        help="Agent to install for. Repeat for several; defaults to codex.",
    )
    targets = parser.parse_args().target or ["codex"]
    if "all" in targets:
        return list(TARGETS)
    return list(dict.fromkeys(targets))


def ignore_for(target, source):
    if target == "codex":
        return None

    def ignore(directory, names):
        relative = Path(directory).relative_to(source)
        return {name for name in names if relative / name in CODEX_ONLY_FILES}

    return ignore


def prune_empty_dirs(root):
    for directory in sorted(root.rglob("*"), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()


def install(target, install_root, sources):
    install_root.mkdir(parents=True, exist_ok=True)

    for source in sources:
        destination = install_root / source.name

        if destination.is_symlink():
            raise SystemExit(
                f"Refusing to replace symlinked skill destination: {destination}"
            )
        if destination.exists() and not destination.is_dir():
            raise SystemExit(f"Skill destination is not a directory: {destination}")

        staged = install_root / f".{source.name}.installing"
        if staged.exists():
            if staged.is_symlink() or not staged.is_dir():
                staged.unlink()
            else:
                shutil.rmtree(staged)

        ignore = ignore_for(target, source)
        shutil.copytree(source, staged, ignore=ignore)
        if ignore:
            prune_empty_dirs(staged)

        if destination.exists():
            shutil.rmtree(destination)

        staged.replace(destination)
        print(f"Installed {source.name} ({target}) -> {destination}")


targets = parse_targets()

if not source_root.is_dir():
    raise SystemExit(f"Skills source directory not found: {source_root}")

sources = sorted(path for path in source_root.iterdir() if path.is_dir())
if not sources:
    raise SystemExit(f"No skill directories found under: {source_root}")

for source in sources:
    if not (source / "SKILL.md").is_file():
        raise SystemExit(f"Missing SKILL.md: {source}")

for target in targets:
    install(target, TARGETS[target](), sources)
