# Auto File Organizer 🗂️

> "I hate cleaning my Downloads folder, so I built this."

This small Python script automatically organizes files in a folder by moving them into subfolders based on **file type** and optionally by **date**.

Perfect for messy folders like `Downloads`, `Desktop`, or project dumps.

---

## ✨ Features

- Organizes files into categories like:
  - `Documents`, `Images`, `Videos`, `Audio`, `Archives`, `Code`, `PDFs`, `Others`
- Optional **date-based grouping** → creates `YYYY-MM` subfolders (e.g., `2025-12`)
- Optional **recursive mode** → include subfolders
- **Dry-run mode** to preview moves without changing anything
- Automatically **resolves name conflicts** by adding suffixes like `file_(1).txt`

---

## 🛠️ Installation

Requirements:
- Python 3.8+

Clone the repository:

```bash
git clone https://github.com/<your-username>/auto-file-organizer.git
cd auto-file-organizer
