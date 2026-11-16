import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3.1-flash-lite"

def gerar(prompt: str, tools=None) -> str:
    """Chama o Gemini. Se tools for passado, habilita tool calling."""
    config = None
    if tools:
        config = types.GenerateContentConfig(
            tools=tools,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False),
        )
    resp = _client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config,
    )
    return resp.text