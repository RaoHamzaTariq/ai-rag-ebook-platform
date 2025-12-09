from agents import OpenAIChatCompletionsModel,RunConfig
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY=os.getenv("GOOGLE_API_KEY")

external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=external_client)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
