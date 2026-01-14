# pxel ⚡ — Smart Package Installer

`pxel` is a **single-file installer helper** that tries to install packages
the *best possible way* for your system and explains failures in plain English.

Made to reduce terminal rage.

---

## Why pxel exists

Installing packages can fail because of:
- OS limitations
- CPU architecture
- Unsupported platforms (Termux pain)
- Python / Node mismatch

pxel:
- Detects your environment
- Chooses the best installer
- Falls back safely
- Explains WHY something failed

---

## Usage

Install once (no setup needed):
```bash
python pxel.py
pxel install (package name)
