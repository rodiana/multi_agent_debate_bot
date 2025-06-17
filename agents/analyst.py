from utils.langsmith import load_prompt_from_hub
from langchain_core.runnables import Runnable
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

from langsmith import Client

class AnalystAgent:
    def __init__(self):


        # Load prompt from LangSmith Prompt Hub
        self.prompt: PromptTemplate = load_prompt_from_hub("analyst_prompt")

        # Initialize local LLaMA model
        self.llm = OllamaLLM(model="llama3", temperature=0.7)

        # Chain prompt into LLM
        self.runnable: Runnable = self.prompt | self.llm

    def get_runnable(self) -> Runnable:
        return self.runnable
