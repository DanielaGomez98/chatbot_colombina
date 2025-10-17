import os
import re
from pathlib import Path

project_root = Path(__file__).parent.parent

INPUT_DIR = project_root / "web_scraping" / "md_files"
OUTPUT_DIR = project_root / "preprocessing" / "cleaned_md_files"
UNIFIED_FILE = project_root / "knowledge_base" / "knowledge_base.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_markdown(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", "", text)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"http\S+|www\.\S+", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"^\|.*\|$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[\^?\d+\]:?.*", "", text)
    text = re.sub(r"[•\*\-\_]{2,}", "", text)
    text = re.sub(r"[ \t]+", " ", text)

    lines = [line.strip() for line in text.splitlines()]
    seen = set()
    unique_lines = [line for line in lines if line and not (line in seen or seen.add(line))]

    clean_lines = []
    buffer_list = []

    for line in unique_lines:
        if re.match(r"^(\-|\*|\+|\d+\.)\s", line) or line.startswith("• "):
            item_text = re.sub(r"^(\-|\*|\+|\d+\.)\s*|^•\s*", "", line)
            buffer_list.append(item_text)
        else:
            if buffer_list:
                joined = ". ".join(buffer_list).strip() + "."
                clean_lines.append(joined)
                buffer_list = []
            if line:
                clean_lines.append(line)

    if buffer_list:
        joined = ". ".join(buffer_list).strip() + "."
        clean_lines.append(joined)

    return "\n".join(clean_lines)

def process_and_unify_with_titles(input_dir: str, output_dir: str, unified_path: str):
    all_clean_texts = []

    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".md"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            with open(input_path, "r", encoding="utf-8") as f:
                content = f.read()

            cleaned = clean_markdown(content)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(cleaned)

            title = os.path.splitext(filename)[0]
            all_clean_texts.append(f"=== {title} ===\n{cleaned}")
            print(f"{filename} listo.")

    with open(unified_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_clean_texts))

    print(f"\n📄 Archivo unificado creado: {unified_path}")

if __name__ == "__main__":
    process_and_unify_with_titles(INPUT_DIR, OUTPUT_DIR, UNIFIED_FILE)
