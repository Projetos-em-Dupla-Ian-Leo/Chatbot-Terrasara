CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco_kg REAL NOT NULL,
    estoque_kg REAL NOT NULL,
    organico INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    criado_em TEXT NOT NULL DEFAULT (datetime('now')),
    status TEXT NOT NULL DEFAULT 'confirmado',
    total REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS itens_pedido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
    produto_id INTEGER NOT NULL REFERENCES produtos(id),
    quantidade_kg REAL NOT NULL,
    preco_unitario REAL NOT NULL
);

-- Views seguras
CREATE VIEW IF NOT EXISTS vw_faturamento_semana AS
SELECT
    date(criado_em) AS dia,
    COUNT(*) AS qtd_pedidos,
    SUM(total) AS faturamento
FROM pedidos
WHERE criado_em >= datetime('now', '-7 days')
GROUP BY date(criado_em);

CREATE VIEW IF NOT EXISTS vw_top_produtos AS
SELECT
    p.nome,
    SUM(i.quantidade_kg) AS kg_vendidos,
    SUM(i.quantidade_kg * i.preco_unitario) AS receita
FROM itens_pedido i
JOIN produtos p ON p.id = i.produto_id
GROUP BY p.id
ORDER BY receita DESC
LIMIT 10;