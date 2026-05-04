from ingestion import load_pdfs
from generator import (
    simple_qa_generator,
    multi_hop_generator,
    comparative_generator,
    web_update_generator,
    hypothetical_generator
)
from filters import quality_filter
from evaluators import calculate_coverage
import json

def save_dataset(dataset, filepath="data/datasets/evaluation_dataset_v1.jsonl"):
    with open(filepath, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"Датасет сохранён: {filepath} ({len(dataset)} примеров)")


if __name__ == "__main__":
    
    documents = load_pdfs("data/papers")
    
    if len(documents) == 0:
        print("Нет документов для генерации!")
        exit()

   
    print("Генерация датасета...")
    dataset = []
    
    dataset += simple_qa_generator(documents, n=35)
    dataset += multi_hop_generator(documents, n=40)
    dataset += comparative_generator(documents, n=35)
    dataset += web_update_generator(documents, n=30)
    dataset += hypothetical_generator(documents, n=20)

    
    dataset = quality_filter(dataset, min_score=0.72)
    coverage_report = calculate_coverage(dataset)

    save_dataset(dataset)
    
    print(f"\nИтоговый размер датасета: {len(dataset)} примеров")