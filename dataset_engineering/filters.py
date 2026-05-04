from langchain_openai import ChatOpenAI
from typing import List, Dict
from config import LLM_MODEL, API_KEY
llm_judge = ChatOpenAI(model=LLM_MODEL, base_url="https://routerai.ru/api/v1", api_key=API_KEY, temperature=0)

def quality_filter(dataset: List[Dict], min_score: float = 0.85) -> List[Dict]:
    filtered = []
    
    for item in dataset:
        prompt = f"""
        Оцени качество вопроса от 0 до 1 по критериям:
        - Ясность и понятность
        - Научная ценность
        - Подходит для RAG-системы
        - Требует reasoning

        Вопрос: {item['question']}
        
        Верни только число от 0.0 до 1.0:
        """
        try:
            score = float(llm_judge.invoke(prompt).content.strip())
            if score >= min_score:
                filtered.append(item)
        except:
            continue
    
    print(f"После фильтрации осталось {len(filtered)} из {len(dataset)} примеров")
    return filtered