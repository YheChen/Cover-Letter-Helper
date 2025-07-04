# LaTeX Cover Letter Generator

Generate beautifully formatted, personalized cover letters using a LaTeX template, a CSV file, and optional signature image all from the command line.

---

## Features

- Fill in placeholders like `[Company]` and `[Title]` from a CSV file
- Include a signature.png file in /example
- Generate one PDF per entry
- Output clean, production-ready PDFs into a specified folder (default: `letters/`)
- Signature image is optional
- LaTeX build files (`.aux`, `.log`, `.tex`, etc.) are cleaned up automatically

---

## Requirements

- Python 3.6+
- A working LaTeX installation with `pdflatex` in your system path
  - [MiKTeX (Windows)](https://miktex.org/download)
  - [TeX Live (macOS/Linux)](https://tug.org/texlive/)

---

## Quick Start

### 1. Clone or download this repo

```bash
git clone https://https://github.com/YheChen/Cover-Letter-Helper
cd Cover-Letter-Helper
python generate.py --csv example/data.csv --template example/template.tex --image example/signature.png --out letters
```
