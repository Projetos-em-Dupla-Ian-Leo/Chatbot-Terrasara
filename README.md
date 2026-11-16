# Terrasara Assistant 🌱

Agente de IA para hortifruti orgânico: atende clientes (FAQ + pedidos) e o dono (gestão), com **tool calling** sobre banco relacional, **orquestração de agentes** e **views seguras** por perfil.

> Projeto de portfólio focado em **IA aplicada a negócio** — construído para demonstrar orquestração de agentes, automação e análise de dados com IA.

---

## 🎯 Problema

Pequenos hortifrutis orgânicos recebem muitas mensagens repetitivas (preço, entrega, estoque) e o dono não tem tempo de responder tudo nem de consolidar as vendas. O Terrasara Assistant:

- Responde **FAQ** automaticamente (entrega, horário, orgânico).
- Consulta **preço e estoque reais** no banco (não inventa).
- Dá ao dono **faturamento da semana** e **top produtos** via linguagem natural, lendo apenas **views seguras**.
- Transfere para **humano** quando necessário.

---

## 🏗️ Arquitetura
Usuário (CLI / Telegram)
│
▼
┌─────────────┐
│ Roteador │ (LLM classifica intenção: FAQ / PEDIDOS / DONO / HUMANO)
└──────┬──────┘
│
┌──────┼──────────────┬──────────────┐
▼ ▼ ▼ ▼
FAQ PEDIDOS DONO HUMANO
│ │
▼ ▼
tools: buscar_produto, consultar_preco, consultar_estoque
tools: faturamento_semana, top_produtos (views seguras)
│
▼
SQLite (produtos, pedidos, itens_pedido + views vw_*)

flowchart TD
    U[Usuário] --> R[Roteador LLM]
    R -->|FAQ| F[Agente FAQ]
    R -->|PEDIDOS| P[Agente Pedidos]
    R -->|DONO| D[Agente Dono]
    R -->|HUMANO| H[Transferência para humano]
    P --> T1[buscar_produto]
    P --> T2[consultar_preco]
    P --> T3[consultar_estoque]
    D --> T4[faturamento_semana]
    D --> T5[top_produtos]
    T1 --> DB[(SQLite)]
    T2 --> DB
    T3 --> DB
    T4 --> V[(Views seguras vw_*)]
    T5 --> V

mais compacto

flowchart TD
    U[Usuário] --> R{Roteador LLM}
    R -->|FAQ| F[Agente FAQ]
    R -->|PEDIDOS| P[Agente Pedidos]
    R -->|DONO| D[Agente Dono]
    R -->|HUMANO| H[Transferência]
    P --> T[Tools: buscar_produto / consultar_preco / consultar_estoque]
    D --> S[Views seguras: faturamento_semana / top_produtos]
    T --> DB[(SQLite)]
    S --> DB

**Stack:** Python · FastAPI · Google Gemini (`google-genai`) · SQLite · pytest · Git

---

## 🧠 Decisões técnicas

- **Tool calling em vez de RAG:** o preço vem do banco (`consultar_preco`), nunca do LLM. Elimina alucinação de preço.
- **Views seguras (`vw_*`):** o agente do dono só lê views agregadas, simulando permissões por perfil. Cobre requisito de **segurança** e **análise de dados com IA**.
- **Roteador separado dos agentes:** cada agente tem seu próprio prompt e ferramentas. Facilita evoluir e testar isoladamente.
- **Prompts versionados em `prompts/*.txt`:** prompt engineering tratado como código, não como string solta.
- **Dados sintéticos no repo:** a estrutura é baseada no projeto acadêmico Terrasara; dados reais ficam fora por privacidade (`db/seed.py` gera tudo).

---

## 🧪 Testes

```bash
pytest -v

Cobertura atual: 14 testes (7 de tools, 4 de roteamento, 3 de prompt injection), todos passando.

test_tools.py — valida busca, preço, estoque, faturamento e top produtos contra o banco.

test_router.py — valida classificação de intenção com o LLM.

test_injection.py — valida que o agente resiste a "ignore instruções", produto inexistente e pedido de dados de cliente

🚀 Como rodar

# 1. clonar e entrar
git clone <seu-repo>
cd terrasara-agent

# 2. ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1      # Windows
# source .venv/bin/activate       # Linux/Mac

# 3. dependências
pip install -r requirements.txt

# 4. configurar chave do Gemini
# crie .env a partir de .env.example e preencha GEMINI_API_KEY

# 5. criar banco com dados sintéticos
python db/seed.py

# 6. rodar o agente no terminal
python -m app.cli

# 7. (opcional) rodar testes
pytest -v

# 8. (opcional) rodar o bot no Telegram
python -m app.bot

Exemplo de conversa:

Você: Quanto custa a banana?
[PEDIDOS] Assistente: A banana prata orgânica custa R$ 7,90 o quilo. Gostaria de adicionar à sua cesta?

Você: Qual foi o faturamento da semana?
[DONO] Assistente: O faturamento desta semana foi de R$ 710,20, com 28 pedidos.
- 10/11: R$ 214,48 (7 pedidos)
- 11/11: R$ 40,18 (4 pedidos)
...

👤 Autor
Ian — estudante de ADS (FATEC Mogi das Cruzes)
LinkedIn · GitHub