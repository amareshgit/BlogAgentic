from langchain_groq import ChatGroq

import os
from dotenv import load_dotenv

class GroqLLM:
    def __init__(self):
        load_dotenv()
        self.groq_api_key = os.getenv("GROQ_API_KEY")

    def get_llm(self):
       try:
          llm = ChatGroq(api_key=self.groq_api_key, model="openai/gpt-oss-20b")
          return llm
       except Exception as e:
        raise ValueError(f"Error initializing Groq LLM: {e}") 


 