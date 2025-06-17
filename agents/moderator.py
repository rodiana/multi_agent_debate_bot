# agents/moderator.py

from utils.langsmith import load_prompt_from_hub
from langchain_core.runnables import Runnable
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

class ModeratorAgent:
    def __init__(self):
        self.prompt: PromptTemplate = load_prompt_from_hub("moderator_prompt")
        self.llm = OllamaLLM(model="llama3", temperature=0.3)  # Lower temp for neutrality
        self.runnable: Runnable = self.prompt | self.llm

    def get_runnable(self) -> Runnable:
        return self.runnable
