#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

repo_root = Path(__file__).resolve().parents[1]
source_root = repo_root / "skills"

codex_home_value = os.environ.get("CODEX_HOME")
if codex_home_value:
    codex_home = Path(codex_home_value).expanduser()
else:
    codex_home = Path.home() / ".codex"

install_root_value = os.environ.get("CODEX_SKILLS_DIR")
if install_root_value:
    install_root = Path(install_root_value).expanduser()
else:
    install_root = codex_home / "skills"

if not source_root.is_dir():
    raise SystemExit(f"Skills source directory not found: {source_root}")

sources = sorted(path for path in source_root.iterdir() if path.is_dir())
if not sources:
    raise SystemExit(f"No skill directories found under: {source_root}")

for source in sources:
    if not (source / "SKILL.md").is_file():
        raise SystemExit(f"Missing SKILL.md: {source}")

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

    shutil.copytree(source, staged)

    if destination.exists():
        shutil.rmtree(destination)

    staged.replace(destination)
    print(f"Installed {source.name} -> {destination}")
