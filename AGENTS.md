# Skill maintenance

This repository is the source of truth for personal, cross-project skills.

- Keep each skill focused, stack-neutral where possible, and useful across more than one project.
- Add a rule only when it changes a decision and is supported by a concrete, reusable lesson.
- For a proposed lesson, retain the trigger, mechanism, conditions, evidence, and trade-off. Do not have a skill edit itself or append lessons automatically.
- Check for overlap before adding a new skill or rule; prefer a narrow update to an existing skill when ownership is clear.
- Keep project-specific conventions in that project's guidance rather than generalizing them here.
- Validate changed skills with the Codex skill validator before installing them. Skills are also installed for Claude Code and Antigravity, so keep instructions tool-neutral and front matter limited to `name` and `description`.
- Edit skills in this repository, then run the installer (`--target codex|claude|antigravity|all`) to refresh the local copies. Do not edit generated copies directly.
- Do not commit or push changes unless the user asks.
