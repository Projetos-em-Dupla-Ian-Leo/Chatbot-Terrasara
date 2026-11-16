from app.router import responder

def main():
    print("Terrasara Assistant (CLI). Digite 'sair' para encerrar.\n")
    while True:
        msg = input("Você: ").strip()
        if msg.lower() in ("sair", "exit", "quit"):
            break
        if not msg:
            continue
        try:
            intencao, resposta = responder(msg)
            print(f"[{intencao}] Assistente: {resposta}\n")
        except Exception as e:
            print(f"[ERRO] {type(e).__name__}: {e}\n")

if __name__ == "__main__":
    main()