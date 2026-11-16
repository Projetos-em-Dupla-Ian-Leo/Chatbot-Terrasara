from pathlib import Path
from app.llm import gerar

PROMPT = Path("prompts/faq.txt").read_text(encoding="utf-8")

def responder(mensagem: str) -> str:
    return gerar(f"{PROMPT}\n\nCliente: {mensagem}\nAssistente:")