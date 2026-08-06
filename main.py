import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = "8800032771:AAFWu64ryPTZB5GWjvFy4ym7xMyKo7JthSQ"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_prompt = update.message.text
    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt
    )
    await update.message.reply_text(response.text)

if __name__ == "__main__":
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(echo_handler)
    application.run_polling()
