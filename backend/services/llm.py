from configs.logger import logger
from pydantic_ai import Agent
from pydantic_ai.messages import ModelResponse
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from .exceptions import *

load_dotenv()

def initialize_agent(
    sys_prompt: str, output_type: Optional[BaseModel] = None, model: str = "gemini-1.5-flash"
) -> Optional["Agent"]:
    GOOGLE_API_KEY = os.environ.get("GEMINI_KEY")

    try:
        provider = GoogleProvider(api_key=GOOGLE_API_KEY)
        model = GoogleModel(model_name=model, provider=provider)
        return Agent(model=model, system_prompt=sys_prompt, output_type=output_type)
    except Exception as e:
        logger.error(f"initialize_agent failed: {e}")
        raise AgentInitError(e)


def call_llm(agent: "Agent", prompt: str) -> "ModelResponse":
    try:
        return agent.run_sync(user_prompt=prompt)
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise LLMCallError(e)
