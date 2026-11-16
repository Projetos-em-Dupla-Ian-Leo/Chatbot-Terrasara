import sqlite3, random, os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
DB = os.getenv("DB_PATH", "db/terrasara.db")
random.seed(42)

PRODUTOS = [
    ("Banana Prata", "fruta", 7.90, 40),
    ("Maca Fuji", "fruta", 12.50, 25),
    ("Alface Crespa", "verdura", 4.50, 15),
    ("Tomate Italiano", "legume", 9.90, 20),
    ("Cenoura", "legume", 5.50, 30),
    ("Brocolis", "verdura", 11.00, 10),
    ("Laranja Pera", "fruta", 6.80, 35),
    ("Batata Doce", "legume", 6.20, 28),
]

def main():
    conn = sqlite3.connect(DB)
    with open("db/schema.sql", encoding="utf-8") as f:
        conn.executescript(f.read())
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM produtos")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO produtos (nome, categoria, preco_kg, estoque_kg) VALUES (?,?,?,?)",
            PRODUTOS,
        )
        for _ in range(30):
            dias = random.randint(0, 6)
            data = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d %H:%M:%S")
            itens = random.sample(PRODUTOS, k=random.randint(1, 3))
            total = 0
            pedido_id = cur.execute(
                "INSERT INTO pedidos (cliente, criado_em, total) VALUES (?,?,0)",
                (f"Cliente {random.randint(1,99)}", data),
            ).lastrowid
            for nome, cat, preco, _ in itens:
                qtd = round(random.uniform(0.5, 3.0), 1)
                pid = cur.execute("SELECT id FROM produtos WHERE nome=?", (nome,)).fetchone()[0]
                cur.execute(
                    "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade_kg, preco_unitario) VALUES (?,?,?,?)",
                    (pedido_id, pid, qtd, preco),
                )
                total += qtd * preco
            cur.execute("UPDATE pedidos SET total=? WHERE id=?", (round(total, 2), pedido_id))
    conn.commit()
    conn.close()
    print("Banco pronto:", DB)

if __name__ == "__main__":
    main()