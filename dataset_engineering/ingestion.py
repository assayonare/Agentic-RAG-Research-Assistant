import os
from llama_index.core import SimpleDirectoryReader
from typing import List
from llama_index.core.schema import Document

def load_pdfs(directory: str = "data/papers") -> List[Document]:
    """Загружает все PDF из папки"""
    if not os.path.exists(directory):
        # os.makedirs(directory, exist_ok=True)
        print(f"Папка {directory} не создана")
        return []

    reader = SimpleDirectoryReader(
        input_dir=directory,
        required_exts=[".pdf"],
        recursive=True
    )
    documents = reader.load_data()
    print(f"Загружено {len(documents)} документов из {directory}")
    return documents