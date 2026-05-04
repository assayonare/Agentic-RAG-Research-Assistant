from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict
from llama_index.core.schema import Document
import uuid
import json
import re
from config import LLM_MODEL, API_KEY

llm = ChatOpenAI(
    model=LLM_MODEL,
    base_url="https://routerai.ru/api/v1",
    api_key=API_KEY,
    temperature=0.7
)


def _clean_json_response(response_text: str) -> str:
    """Очищает ответ от markdown и лишнего текста"""
    response_text = re.sub(r'```json\s*', '', response_text)
    response_text = re.sub(r'```\s*', '', response_text)
    return response_text.strip()


def _generate_questions(docs: List[Document], prompt_template: str, n: int, category: str) -> List[Dict]:
    questions = []
    texts = [doc.text for doc in docs if len(doc.text) > 800]
    
    if not texts:
        return []

    prompt = ChatPromptTemplate.from_template(prompt_template)
    chain = prompt | llm

    batch_size = 6
    batches = (n + batch_size - 1) // batch_size

    for batch in range(batches):
        current_n = min(batch_size, n - len(questions))
        if current_n <= 0:
            break

        text_sample = texts[batch % len(texts)]

        response = chain.invoke({
            "text": text_sample[:18000],
            "num_questions": current_n,
            "category": category  # передаём категорию в промпт
        })

        try:
            cleaned = _clean_json_response(response.content)
            data = json.loads(cleaned)

            if isinstance(data, dict) and "questions" in data:
                items = data["questions"]
            else:
                items = data if isinstance(data, list) else [data]

            for item in items:
                if isinstance(item, dict) and "question" in item:
                    q_text = item["question"].strip()
                    if len(q_text) > 40:
                        questions.append({
                            "id": str(uuid.uuid4()),
                            "category": category,
                            "category_number": len(questions) + 1,
                            "global_number": None,                
                            "question": q_text,
                            # "ground_truth": "",
                            # "gold_contexts": [text_sample[:2800]],
                            "domain": "AI/ML",
                            "language": "ru" if any(word in q_text.lower() 
                                                  for word in ["россий", "русский", "в россии", "россия"]) else "en",
                            # "tags": [category]
                        })
        except Exception as e:
            print(f"Ошибка парсинга JSON в категории {category}: {e}")
            continue

    return questions[:n]


def simple_qa_generator(documents: List[Document], n: int = 35):
    prompt = """
Ты — эксперт по созданию оценочных датасетов для Agentic RAG систем.
На основе предоставленного текста создай {num_questions} простых, но осмысленных вопросов.

Требования:
- Вопросы должны требовать извлечения конкретной информации
- Разнообразные формулировки
- Научный стиль

Текст: {text}

Верни ответ **строго в JSON формате**:
{{
  "questions": [
    {{"question_number": 1, "question": "Вопрос здесь..."}},
    {{"question_number": 2, "question": "Вопрос здесь..."}}
  ]
}}
"""
    return _generate_questions(documents, prompt, n, "simple")


def multi_hop_generator(documents: List[Document], n: int = 40):
    prompt = """
Создай {num_questions} сложных multi-hop вопросов, которые требуют объединения информации из разных частей текста.

Текст: {text}

Верни ответ **строго в JSON формате**:
{{
  "questions": [
    {{"question_number": 1, "question": "Вопрос здесь..."}},
    {{"question_number": 2, "question": "Вопрос здесь..."}}
  ]
}}
"""
    return _generate_questions(documents, prompt, n, "multi_hop")


def comparative_generator(documents: List[Document], n: int = 35):
    prompt = """
Создай {num_questions} вопросов, которые требуют сравнения методов, результатов, подходов или моделей из текста.

Текст: {text}

Верни ответ **строго в JSON формате**:
{{
  "questions": [
    {{"question_number": 1, "question": "Вопрос здесь..."}},
    {{"question_number": 2, "question": "Вопрос здесь..."}}
  ]
}}
"""
    return _generate_questions(documents, prompt, n, "comparative")


def web_update_generator(documents: List[Document], n: int = 30):
    prompt = """
Создай {num_questions} вопросов, которые требуют свежей информации 2025–2026 годов 
(что изменилось, новые работы, развитие идеи после этой статьи и т.д.).

Текст: {text}

Верни ответ **строго в JSON формате**:
{{
  "questions": [
    {{"question_number": 1, "question": "Вопрос здесь..."}},
    {{"question_number": 2, "question": "Вопрос здесь..."}}
  ]
}}
"""
    return _generate_questions(documents, prompt, n, "web_update")


def hypothetical_generator(documents: List[Document], n: int = 20):
    prompt = """
Создай {num_questions} гипотетических, exploratory или "what if" вопросов, 
а также вопросов на предложение экспериментов на основе текста.

Текст: {text}

Верни ответ **строго в JSON формате**:
{{
  "questions": [
    {{"question_number": 1, "question": "Вопрос здесь..."}},
    {{"question_number": 2, "question": "Вопрос здесь..."}}
  ]
}}
"""
    return _generate_questions(documents, prompt, n, "hypothetical")