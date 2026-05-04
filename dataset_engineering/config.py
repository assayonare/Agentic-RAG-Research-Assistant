from dotenv import load_dotenv
import os

load_dotenv()

LLM_MODEL = "deepseek/deepseek-v3.2"
TEMPERATURE = 0.7
MAX_TOKENS = 2000
API_KEY = os.getenv("API_KEY")
TARGET_PROPORTIONS = {
    "simple": 0.20,
    "multi_hop": 0.25,
    "comparative": 0.25,
    "exploratory": 0.15,
    "hypothetical": 0.15,
}