# agents-skills

Personal, cross-project agent skills for Codex, Claude Code, and Antigravity. This repository is the source of truth; installed copies are generated from it.

## Install or refresh

From the repository root, run the installer for the agents you use:

```sh
python3 scripts/install_skills.py                         # Codex (default)
python3 scripts/install_skills.py --target claude         # Claude Code
python3 scripts/install_skills.py --target antigravity    # Antigravity
python3 scripts/install_skills.py --target all            # all three
```

`--target` can be repeated. Each target installs to its global skills directory:

| Target | Default destination | Override |
| --- | --- | --- |
| `codex` | `${CODEX_HOME:-$HOME/.codex}/skills` | `CODEX_SKILLS_DIR` |
| `claude` | `${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills` | `CLAUDE_SKILLS_DIR` |
| `antigravity` | `$HOME/.gemini/config/skills` | `ANTIGRAVITY_SKILLS_DIR` |

Older standalone Antigravity IDE builds read `~/.gemini/antigravity/skills`; set `ANTIGRAVITY_SKILLS_DIR` to that path if yours does not pick up skills from the default.

Run the installer after cloning, pulling, or changing a skill. It replaces only same-named skill folders and leaves other installed skills alone. Deleting a skill from this repository does not uninstall its local copies. Codex-only metadata (`agents/openai.yaml`) is installed only for the `codex` target.

All three agents load a skill automatically when a request matches its description. You can also invoke one directly: `$skill-name` in Codex, `/skill-name` in Claude Code, or by naming the skill in an Antigravity prompt.

## Export a transcript

Export a local Codex session and its subagent sessions for evaluation (Python 3.11+):

```sh
python3 scripts/extract_transcript.py SESSION_ID --output ~/Desktop/transcript.txt
```

The script accepts a session ID or JSONL path and searches active and archived logs under `CODEX_HOME` (default `~/.codex`). It exports public messages and tool activity, excluding private reasoning and system/developer instructions. Use `--until` to stop at a timestamp, `--include-nested-tools` for additional command/connector records, or `--no-subagents` for one session. Existing output files are never overwritten.

Exports can contain sensitive user/tool text. `--redact-file` accepts one literal value per line to replace with `[REDACTED]`; it is not an automatic secret detector. Run `--help` for all options. This utility stays in the repository and is not installed with skills.

## Bundled skills

These skills are maintained in this repository and installed by the script above.

| Skill | Useful for |
| --- | --- |
| [review-and-refine](skills/review-and-refine/SKILL.md) | Coordinating independent reviews and optional iterative fixes through an approved plan, with model choice, scope control, and goal-mode support. |
| [untangle-codebase](skills/untangle-codebase/SKILL.md) | Diagnosing structural coupling and unnecessary indirection, then refactoring within an agreed scope while preserving behavior. |
| [performance-aware-coding](skills/performance-aware-coding/SKILL.md) | Spotting likely runtime costs during implementation or review, then validating meaningful optimizations with evidence. |
| [brand-domain-research](skills/brand-domain-research/SKILL.md) | Brainstorming brand and product names, suggesting matching domains, and checking registration records with RDAP when requested. |

## Add a skill

Add `skills/<name>/SKILL.md` with `name` (matching the folder; lowercase letters, digits, and hyphens) and `description` front matter. Keep instructions tool-neutral so they work in Codex, Claude Code, and Antigravity. Include `agents/openai.yaml` (Codex-only) or supporting files only when needed. Keep changes evidence-based and review them before installing.

## External recommendations

These skills are maintained outside this repository and are not copied or installed here. Check each upstream source for current installation and license details.

| Skill | Useful for | Upstream source |
| --- | --- | --- |
| `browse-x` | Reading public X posts, threads, profiles, and search results as Markdown or JSON. | [pc-style/x-md](https://github.com/pc-style/x-md/tree/main/skills/browse-x) |
| `security-best-practices` | Applying language- and framework-specific secure coding guidance. | [openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) |
| `security-threat-model` | Mapping a repository's trust boundaries, assets, attacker paths, and mitigations. | [openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model) |
| `prune-tests` | Finding brittle or tautological tests and removing them when cleanup is authorized. | [riffingonsoftware/agent-skills](https://github.com/riffingonsoftware/agent-skills/tree/trunk/skills/prune-tests) |
| `security-audit` | Running a structured, source-grounded security audit. | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill/tree/main/skills/security-audit) |

## License

This repository is licensed under the MIT License. See [LICENSE](LICENSE).
