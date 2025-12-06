#!/usr/bin/env python3
"""
Auto File Organizer

"I hate cleaning my Downloads folder, so I built this."

This script automatically organizes files in a given folder by:
- Grouping files into subfolders based on file type (Documents, Images, Videos, etc.)
- Optional: adding date-based subfolders (YYYY-MM) inside each category
- Optional: recursive mode to include subfolders
- Dry-run mode to preview actions without actually moving files

Usage:
    python organize.py --path "C:/Users/You/Downloads"
    python organize.py --path "/home/you/Downloads" --by-date
    python organize.py --path "./test-folder" --recursive --dry-run
"""

import argparse
import os
import shutil
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Mapping of extension -> category
EXTENSION_MAP = {
    "Documents": [
        ".txt", ".doc", ".docx", ".odt", ".rtf", ".md"
    ],
    "Spreadsheets": [
        ".xls", ".xlsx", ".ods", ".csv"
    ],
    "Presentations": [
        ".ppt", ".pptx", ".odp"
    ],
    "PDFs": [
        ".pdf"
    ],
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp"
    ],
    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm"
    ],
    "Audio": [
        ".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz"
    ],
    "Code": [
        ".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".php",
        ".html", ".css", ".json", ".ipynb"
    ]
}


def detect_category(file_path: Path) -> str:
    ext = file_path.suffix.lower()
    for category, ext_list in EXTENSION_MAP.items():
        if ext in ext_list:
            return category
    return "Others"


def get_date_folder(file_path: Path) -> str:
    """Return folder name like '2025-12' based on last modified time."""
    ts = file_path.stat().st_mtime
    dt = datetime.fromtimestamp(ts)
    return dt.strftime("%Y-%m")


def organize_folder(
    base_path: Path,
    by_date: bool = False,
    recursive: bool = False,
    dry_run: bool = False
):
    if not base_path.exists() or not base_path.is_dir():
        raise ValueError(f"Path does not exist or is not a directory: {base_path}")

    print(f"\n📂 Organizing folder: {base_path}")
    print(f"   Recursive: {recursive}, By date: {by_date}, Dry run: {dry_run}\n")

    moved_files_count = 0
    skipped_files_count = 0
    summary = defaultdict(int)

    if recursive:
        walker = base_path.rglob("*")
    else:
        walker = base_path.iterdir()

    for item in walker:
        # Skip directories
        if item.is_dir():
            # Do not skip here in recursive mode, rglob will dive in
            continue

        # Skip files inside .kiro or other internal folders
        if ".kiro" in item.parts:
            continue

        category = detect_category(item)
        target_dir = base_path / category

        if by_date:
            date_folder = get_date_folder(item)
            target_dir = target_dir / date_folder

        # Avoid moving files that are already in the correct folder
        if item.parent == target_dir:
            skipped_files_count += 1
            continue

        # Create target directory if needed
        if not target_dir.exists() and not dry_run:
            target_dir.mkdir(parents=True, exist_ok=True)

        target_path = target_dir / item.name

        # Handle name collisions
        if target_path.exists():
            # Add a suffix to filename
            stem = target_path.stem
            suffix = target_path.suffix
            counter = 1
            while True:
                new_name = f"{stem}_({counter}){suffix}"
                new_target = target_dir / new_name
                if not new_target.exists():
                    target_path = new_target
                    break
                counter += 1

        # Move or simulate
        if dry_run:
            print(f"[DRY-RUN] Would move: {item} -> {target_path}")
        else:
            print(f"Moving: {item} -> {target_path}")
            shutil.move(str(item), str(target_path))

        moved_files_count += 1
        summary[category] += 1

    print("\n✅ Done!")
    print(f"Total files moved : {moved_files_count}")
    print(f"Files already in place / skipped: {skipped_files_count}")
    if summary:
        print("\nBreakdown by category:")
        for cat, count in summary.items():
            print(f"  - {cat}: {count} file(s)")
    else:
        print("No files were moved.")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Auto File Organizer - organize files by type (and optionally date)."
    )
    parser.add_argument(
        "--path",
        "-p",
        required=True,
        help="Path to the folder you want to organize."
    )
    parser.add_argument(
        "--by-date",
        action="store_true",
        help="Also group files into YYYY-MM subfolders based on modified date."
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Include files from subdirectories as well."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would happen without actually moving any files."
    )

    return parser.parse_args()


def main():
    args = parse_args()
    base_path = Path(args.path).expanduser().resolve()

    try:
        organize_folder(
            base_path=base_path,
            by_date=args.by_date,
            recursive=args.recursive,
            dry_run=args.dry_run
        )
    except ValueError as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
