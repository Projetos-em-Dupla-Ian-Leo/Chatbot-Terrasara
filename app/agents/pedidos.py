from pathlib import Path
from app.llm import gerar
from app.tools import catalogo

PROMPT = Path("prompts/pedidos.txt").read_text(encoding="utf-8")

TOOLS = [
    catalogo.buscar_produto,
    catalogo.consultar_preco,
    catalogo.consultar_estoque,
]

def responder(mensagem: str) -> str:
    prompt = f"{PROMPT}\n\nCliente: {mensagem}\nAssistente:"
    return gerar(prompt, tools=TOOLS)