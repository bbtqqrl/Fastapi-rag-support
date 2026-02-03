import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
llm_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))