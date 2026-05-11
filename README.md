# Wireless Tutorials

Animated wireless communication tutorials built with [Manim Community](https://www.manim.community/).

## Prerequisites

- Python 3.10+
- [Homebrew](https://brew.sh) (macOS)
- [FFmpeg](https://ffmpeg.org) (installed automatically)

## Setup

```bash
./setup.sh
source .venv/bin/activate
```

## Render a Tutorial

```bash
manim -pql tutorials/5g-initial-setup/5g_initial_setup.py FiveGInitialSetup
```

| Flag | Meaning |
|------|---------|
| `-p`  | Preview (auto-open player) |
| `-ql` | Low quality (fast render) |
| `-qh` | High quality (final export) |

## Tutorials

| Tutorial | Description | Dir |
|----------|-------------|-----|
| 5G Initial Setup | End-to-end 5G SA initial registration procedure | `tutorials/5g-initial-setup/` |
