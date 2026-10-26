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
