import os
import csv
import subprocess
import shutil
import tempfile
import argparse

def sanitize_filename(name):
    return name.replace(" ", "_").replace("&", "and")

def fill_and_compile(row, template_path, image_path, output_dir):
    company = sanitize_filename(row.get("Company", "Unknown"))
    base = f"Yanzhen_CV_{company}"
    final_pdf_path = os.path.join(output_dir, base + ".pdf")

    with tempfile.TemporaryDirectory() as build_dir:
        tex_file = os.path.join(build_dir, base + ".tex")

        # Fill in the LaTeX template
        with open(template_path, "r", encoding="utf-8") as f:
            tex_content = f.read()

        for key, val in row.items():
            tex_content = tex_content.replace(f"[{key}]", val)

        if "[Signature]" in tex_content:
            if image_path and os.path.exists(image_path):
                image_basename = os.path.basename(image_path)
                tex_content = tex_content.replace("[Signature]", f"\\includegraphics[width=1.1in]{{{image_basename}}}")
                shutil.copy(image_path, os.path.join(build_dir, image_basename))
            else:
                tex_content = tex_content.replace("[Signature]", "")

        with open(tex_file, "w", encoding="utf-8") as f:
            f.write(tex_content)

        # Compile with pdflatex
        subprocess.run(
            [r"C:\Users\Yanzh\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe", 
             "-interaction=nonstopmode", "-output-directory", build_dir, tex_file],
            check=True
        )

        generated_pdf = os.path.join(build_dir, base + ".pdf")
        shutil.move(generated_pdf, final_pdf_path)
        print(f"✅ Created: {final_pdf_path}")

def generate_all(csv_path, template_path, image_path, output_dir="letters"):
    # Clear and create the output folder
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fill_and_compile(row, template_path, image_path, output_dir)

    print(f"\n🎉 All PDFs are in: {os.path.abspath(output_dir)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate LaTeX PDFs from CSV.")
    parser.add_argument("--csv", required=True, help="Path to data.csv")
    parser.add_argument("--template", required=True, help="Path to template.tex")
    parser.add_argument("--image", help="Optional signature image (e.g. signature.png)")
    parser.add_argument("--out", default="letters", help="Output folder (default: letters)")
    args = parser.parse_args()

    generate_all(args.csv, args.template, args.image, args.out)
