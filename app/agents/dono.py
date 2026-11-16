from pathlib import Path
from app.llm import gerar
from app.tools import catalogo

PROMPT = Path("prompts/dono.txt").read_text(encoding="utf-8")

TOOLS = [
    catalogo.faturamento_semana,
    catalogo.top_produtos,
]

def responder(mensagem: str) -> str:
    prompt = f"{PROMPT}\n\nDono: {mensagem}\nAssistente:"
    return gerar(prompt, tools=TOOLS)