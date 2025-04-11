import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load .env variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Without https://
PORT = int(os.getenv("PORT", 8080))

# Simple /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your bot is running successfully.")

# Validate essential variables
if not BOT_TOKEN or not APP_URL:
    raise ValueError("BOT_TOKEN or APP_URL is missing in environment variables!")

# Build bot app
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Register /start handler
app.add_handler(CommandHandler("start", start))

# Run bot using webhook
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,
        webhook_url=f"https://{APP_URL}/{BOT_TOKEN}"
    )
