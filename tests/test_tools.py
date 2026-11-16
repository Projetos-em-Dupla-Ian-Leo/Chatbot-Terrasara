from app.tools import catalogo

def test_buscar_produto_banana():
    res = catalogo.buscar_produto("banana")
    assert isinstance(res, list)
    assert len(res) >= 1
    nomes = [r["nome"].lower() for r in res]
    assert any("banana" in n for n in nomes)

def test_buscar_produto_inexistente():
    res = catalogo.buscar_produto("xyz_nao_existe")
    assert res == []

def test_consultar_preco_existente():
    res = catalogo.consultar_preco(1)
    assert "nome" in res
    assert "preco_kg" in res
    assert res["preco_kg"] > 0

def test_consultar_preco_inexistente():
    res = catalogo.consultar_preco(99999)
    assert "erro" in res

def test_consultar_estoque():
    res = catalogo.consultar_estoque(1)
    assert "estoque_kg" in res
    assert res["estoque_kg"] >= 0

def test_faturamento_semana_estrutura():
    res = catalogo.faturamento_semana()
    assert isinstance(res, list)
    for linha in res:
        assert "dia" in linha
        assert "qtd_pedidos" in linha
        assert "faturamento" in linha

def test_top_produtos_estrutura():
    res = catalogo.top_produtos()
    assert isinstance(res, list)
    assert len(res) >= 1
    for linha in res:
        assert "nome" in linha
        assert "receita" in linha