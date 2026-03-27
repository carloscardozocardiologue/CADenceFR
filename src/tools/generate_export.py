"""
tools/generate_export.py
Generates export_text.MD — a full snapshot of the project for LLM review.
Usage: run from the project root → python tools/generate_export.py
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# ── Configuration ─────────────────────────────────────────────────────────────

# Folders to skip entirely
SKIP_DIRS = {
    ".venv", "venv", "__pycache__", ".git", ".mypy_cache",
    ".pytest_cache", "node_modules", ".streamlit/secrets",
    "dist", "build", ".eggs", "*.egg-info",
}

# Files to skip by name
SKIP_FILES = {
    ".env", ".env.local", ".DS_Store", "Thumbs.db",
    "export_text.MD",           # avoid including a previous export
}

# Extensions to skip (binary / large assets)
SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".pdf", ".xlsx", ".xls", ".csv",
    ".pkl", ".pickle", ".h5", ".parquet",
    ".zip", ".tar", ".gz",
    ".pyc", ".pyo",
    ".lock",                    # package-lock / poetry.lock can be huge
}

# Extensions to include as readable text
TEXT_EXTENSIONS = {
    ".py", ".md", ".txt", ".toml", ".yaml", ".yml",
    ".json", ".ini", ".cfg", ".env.example",
    ".html", ".css", ".js", ".ts", ".jsx", ".tsx",
    ".sh", ".bat", "",          # extensionless files (Makefile, Dockerfile…)
}

OUTPUT_FILE = Path("tools/export_text.MD")
MAX_FILE_BYTES = 100_000        # skip files larger than ~100 KB

# ── Helpers ───────────────────────────────────────────────────────────────────

def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.startswith(".")

def should_skip_file(path: Path) -> bool:
    if path.name in SKIP_FILES:
        return True
    if path.suffix.lower() in SKIP_EXTENSIONS:
        return True
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return True          # unknown extension → skip to be safe
    if path.stat().st_size > MAX_FILE_BYTES:
        return True
    return False

def build_tree(root: Path, prefix: str = "") -> list[str]:
    """Return directory tree lines (like `tree` command)."""
    lines = []
    entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        if entry.is_dir():
            if should_skip_dir(entry.name):
                lines.append(f"{prefix}{connector}{entry.name}/  ← skipped")
                continue
            lines.append(f"{prefix}{connector}{entry.name}/")
            extension = "    " if i == len(entries) - 1 else "│   "
            lines.extend(build_tree(entry, prefix + extension))
        else:
            lines.append(f"{prefix}{connector}{entry.name}")
    return lines

def iter_files(root: Path):
    """Yield all readable files in deterministic order."""
    for path in sorted(root.rglob("*")):
        if path.is_file():
            # Check if any parent dir should be skipped
            if any(should_skip_dir(p.name) for p in path.parents):
                continue
            if should_skip_file(path):
                continue
            yield path

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    root = Path(".").resolve()
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print(f"📦 Generating export from: {root}")
    print(f"📄 Output: {OUTPUT_FILE.resolve()}")

    lines = []

    # Header
    lines.append(f"# Project Export — {root.name}")
    lines.append(f"_Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_\n")
    lines.append("---\n")

    # Directory tree
    lines.append("## 📁 Project Structure\n")
    lines.append("```")
    lines.append(f"{root.name}/")
    lines.extend(build_tree(root))
    lines.append("```\n")
    lines.append("---\n")

    # File contents
    lines.append("## 📄 File Contents\n")

    file_list = list(iter_files(root))
    print(f"   Found {len(file_list)} files to include.")

    for path in file_list:
        rel = path.relative_to(root)
        ext = path.suffix.lower().lstrip(".") or "text"
        lines.append(f"### `{rel}`\n")
        lines.append(f"```{ext}")
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            lines.append(content)
        except Exception as e:
            lines.append(f"[Error reading file: {e}]")
        lines.append("```\n")

    # Write output
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    size_kb = OUTPUT_FILE.stat().st_size / 1024
    print(f"✅ Done! export_text.MD written ({size_kb:.1f} KB, {len(file_list)} files)")

if __name__ == "__main__":
    main()