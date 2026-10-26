# agents-skills

Personal, cross-project Codex skills. This repository is the source of truth; installed copies are generated from it.

## Install or refresh

From the repository root, run:

```sh
python3 scripts/install_skills.py
```

The installer copies skills to `${CODEX_HOME:-$HOME/.codex}/skills`. Set `CODEX_SKILLS_DIR` to override the destination. Run it after cloning, pulling, or changing a skill. It replaces only same-named skill folders and leaves other installed skills alone. Deleting a skill from this repository does not uninstall its local copy.

## Add a skill

Add `skills/<name>/SKILL.md` with the required name and description front matter. Include `agents/openai.yaml` or supporting files only when needed. Keep changes evidence-based and review them before installing.

## External recommendations

These skills are maintained outside this repository and are not copied or installed here. Check each upstream source for current installation and license details.

| Skill | Useful for | Upstream source |
| --- | --- | --- |
| `browse-x` | Reading public X posts, threads, profiles, and search results as Markdown or JSON. | [pc-style/x-md](https://github.com/pc-style/x-md/tree/main/skills/browse-x) |
| `security-best-practices` | Applying language- and framework-specific secure coding guidance. | [openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-best-practices) |
| `security-threat-model` | Mapping a repository's trust boundaries, assets, attacker paths, and mitigations. | [openai/skills](https://github.com/openai/skills/tree/main/skills/.curated/security-threat-model) |
| `prune-tests` | Finding brittle or tautological tests and removing them when cleanup is authorized. | [riffingonsoftware/agent-skills](https://github.com/riffingonsoftware/agent-skills/tree/trunk/skills/prune-tests) |
| `security-audit` | Running a structured, source-grounded security audit. | [cloudflare/security-audit-skill](https://github.com/cloudflare/security-audit-skill/tree/main/skills/security-audit) |
