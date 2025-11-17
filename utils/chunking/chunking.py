import re
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter

project_root = Path(__file__).parent.parent.parent
knowledge_base_path = project_root / "utils" / "knowledge_base" / "improved_knowledge_base.txt"


def load_and_split_docs(filepath=knowledge_base_path):
    """
    Carga el archivo de base de conocimiento y lo divide en documentos individuales
    basados en el delimitador '==='.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        docs_raw = re.split(r'(?m)^=== .* ===$', content)
        docs_raw = [doc for doc in docs_raw if doc.strip()]
        
        delimiters = re.findall(r'(?m)^=== (.*) ===$', content)

        processed_docs = []
        for i, doc_content in enumerate(docs_raw):
            if i < len(delimiters):
                full_doc = f"=== {delimiters[i]} ===\n{doc_content.strip()}"
                processed_docs.append(full_doc)

        print(f"Archivo principal cargado. Se encontraron {len(processed_docs)} documentos individuales.")
        return processed_docs
    
    except FileNotFoundError:
        print(f"Error: El archivo {filepath} no fue encontrado.")
        return []


def parse_document(doc_raw):
    """
    Extrae los metadatos y el contenido principal de un documento delimitado.
    Esta versión está adaptada para la base de conocimiento organizada,
    donde cada sección (=== SECCIÓN ===) contiene texto continuo.
    """
    metadata = {}
    lines = doc_raw.split('\n')

    filename_match = re.search(r'=== (.*) ===', lines[0])
    if filename_match:
        metadata['source_file'] = filename_match.group(1).strip()
        metadata['title'] = metadata['source_file']

    content = "\n".join(lines[1:]).strip()

    return content, metadata


def main():
    """
    Función principal que orquesta el proceso de carga, parsing y chunking.
    """
    documents_raw = load_and_split_docs()
    
    if not documents_raw:
        return

    all_texts = []
    all_metadatas = []

    for doc_raw in documents_raw:
        content, metadata = parse_document(doc_raw)
        if content and metadata.get('title'):
            all_texts.append(content)
            all_metadatas.append(metadata)

    print(f"Se procesaron y parsearon {len(all_texts)} documentos con contenido útil.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = text_splitter.create_documents(all_texts, metadatas=all_metadatas)

    print(f"\n¡Chunking completado! Se generaron {len(chunks)} fragmentos en total.")

    output_chunks = []
    for i, chunk in enumerate(chunks):
        output_chunks.append({
            'chunk_id': i,
            'content': chunk.page_content,
            'metadata': chunk.metadata
        })

    output_filepath = project_root / "utils" / "chunking" / "chunks.json"
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(output_chunks, f, indent=2, ensure_ascii=False)

    print(f"Los chunks se han guardado exitosamente en el archivo: '{output_filepath}'")
    
    print("\n--- Ejemplo de los primeros 2 Chunks ---")
    print(json.dumps(output_chunks[:2], indent=2, ensure_ascii=False))
    print("------------------------------------------")


if __name__ == "__main__":
    main()