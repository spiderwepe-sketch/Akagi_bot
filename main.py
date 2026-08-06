import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 1. Заглушка веб-сервера для удержания порта в Render
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# 2. Переменные авторизации
TELEGRAM_TOKEN = "8800032771:AAFWu64ryPTZB5GWjvFy4ym7xMyKo7JthSQ"

# Берем API-ключ Gemini из переменных окружения Render
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Инициализация клиента
client = genai.Client(api_key=GEMINI_API_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    response = await client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt
    )
    await update.message.reply_text(response.text)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(echo_handler)
    application.run_polling()
