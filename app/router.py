from pathlib import Path
from app.llm import gerar
from app.agents import faq, pedidos, dono

PROMPT = Path("prompts/router.txt").read_text(encoding="utf-8")

def classificar(mensagem: str) -> str:
    saida = gerar(f"{PROMPT}\n\nMensagem: {mensagem}\nIntenção:").strip().upper()
    for opcao in ("FAQ", "PEDIDOS", "DONO", "HUMANO"):
        if opcao in saida:
            return opcao
    return "FAQ"

def responder(mensagem: str) -> tuple[str, str]:
    """Devolve (intenção, resposta)."""
    intencao = classificar(mensagem)
    if intencao == "PEDIDOS":
        return intencao, pedidos.responder(mensagem)
    if intencao == "DONO":
        return intencao, dono.responder(mensagem)
    if intencao == "HUMANO":
        return intencao, "Vou chamar um atendente humano para te ajudar. Aguarde um instante."
    return intencao, faq.responder(mensagem)