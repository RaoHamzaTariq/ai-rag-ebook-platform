from src.agents.triage_agent import triage_agent
import asyncio
from agents import Runner
from src.config.llm import config

async def main():
    result = await Runner.run(triage_agent, "Hi", run_config=config)
    print(result)

asyncio.run(main())

# import asyncio
# from openai import AsyncOpenAI
# from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
# import os 

# from dotenv import load_dotenv
# load_dotenv()
# gemini_api_key = os.getenv("GOOGLE_API_KEY")

# #Reference: https://ai.google.dev/gemini-api/docs/openai
# client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
# )

# set_tracing_disabled(disabled=True)

# async def main():
#     # This agent will use the custom LLM provider
#     agent = Agent(
#         name="Assistant",
#         instructions="You only respond in haikus.",
#         model=OpenAIChatCompletionsModel(model="gemini-2.5-flash-lite", openai_client=client),
#     )

#     result = await Runner.run(
#         agent,
#         "Tell me about recursion in programming.",
#     )
#     print(result.final_output)


# if __name__ == "__main__":
#     asyncio.run(main())