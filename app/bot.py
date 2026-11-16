import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.router import responder

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Olá! Sou o assistente da Terrasara 🌱\n"
        "Pergunte sobre entrega, preços, estoque ou gestão.\n"
        "Digite /ajuda para ver exemplos."
    )

async def ajuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Exemplos:\n"
        "• Vocês entregam no sábado?\n"
        "• Quanto custa a banana?\n"
        "• Qual foi o faturamento da semana?\n"
        "• Quero falar com uma pessoa"
    )

async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    texto = update.message.text or ""
    if not texto.strip():
        return
    try:
        intencao, resposta = responder(texto)
        await update.message.reply_text(f"[{intencao}] {resposta}")
    except Exception as e:
        logging.exception("Erro ao responder")
        await update.message.reply_text("Desculpe, tive um problema técnico. Tente de novo.")

def main() -> None:
    if not TOKEN:
        raise SystemExit("TELEGRAM_TOKEN não configurado no .env")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ajuda", ajuda))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    print("Bot rodando. Vá no Telegram e mande /start para o seu bot. Ctrl+C para parar.")
    app.run_polling()

if __name__ == "__main__":
    main()