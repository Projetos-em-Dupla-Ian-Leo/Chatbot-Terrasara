import sqlite3, os
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DB_PATH", "db/terrasara.db")

def _conn():
    c = sqlite3.connect(DB)
    c.row_factory = sqlite3.Row
    return c

def buscar_produto(termo: str) -> list[dict]:
    """Busca produtos pelo nome (LIKE)."""
    with _conn() as c:
        rows = c.execute(
            "SELECT id, nome, categoria, preco_kg, estoque_kg FROM produtos WHERE nome LIKE ?",
            (f"%{termo}%",),
        ).fetchall()
    return [dict(r) for r in rows]

def consultar_preco(produto_id: int) -> dict:
    with _conn() as c:
        r = c.execute("SELECT nome, preco_kg FROM produtos WHERE id=?", (produto_id,)).fetchone()
    return dict(r) if r else {"erro": "produto não encontrado"}

def consultar_estoque(produto_id: int) -> dict:
    with _conn() as c:
        r = c.execute("SELECT nome, estoque_kg FROM produtos WHERE id=?", (produto_id,)).fetchone()
    return dict(r) if r else {"erro": "produto não encontrado"}

def faturamento_semana() -> list[dict]:
    with _conn() as c:
        rows = c.execute("SELECT * FROM vw_faturamento_semana").fetchall()
    return [dict(r) for r in rows]

def top_produtos() -> list[dict]:
    with _conn() as c:
        rows = c.execute("SELECT * FROM vw_top_produtos").fetchall()
    return [dict(r) for r in rows]