from typing import List, Dict
import json

def calculate_coverage(dataset: List[Dict]) -> Dict:
    from collections import Counter
    categories = [item['category'] for item in dataset]
    stats = dict(Counter(categories))
    
    report = {cat: round(count / len(dataset) * 100, 1) for cat, count in stats.items()}
    # report["total"] = len(dataset)
    
    print("\n=== Coverage Report ===")
    for k, v in report.items():
        print(f"{k}: {v}%")
    
    return report


def balance_dataset(dataset: List[Dict], target_proportions: Dict) -> List[Dict]:

    return dataset