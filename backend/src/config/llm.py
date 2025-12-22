from agents import OpenAIChatCompletionsModel, RunConfig
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key with validation
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")

if not GEMINI_API_KEY:
    logger.warning("Neither GOOGLE_API_KEY nor OPENAI_API_KEY set. The chatbot will fail at runtime until a key is provided.")
    # For now, we'll let it pass to allow the server to start (simple mode)
    # but actual agent runs will fail.
    GEMINI_API_KEY = "PLACEHOLDER_KEY"

# Initialize OpenAI client wih Gemini API
external_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Configure model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# Create run configuration
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)
