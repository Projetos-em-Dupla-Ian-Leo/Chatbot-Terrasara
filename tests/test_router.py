import pytest
from app import router

@pytest.mark.parametrize("mensagem,esperado", [
    ("Vocês entregam no sábado?", "FAQ"),
    ("Quanto custa a banana?", "PEDIDOS"),
    ("Qual foi o faturamento da semana?", "DONO"),
    ("Quero falar com uma pessoa", "HUMANO"),
])
def test_classificacao(mensagem, esperado):
    assert router.classificar(mensagem) == esperado