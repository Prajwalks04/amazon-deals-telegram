import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # e.g., pretty-alisun-shs-creation-bd7184dc.koyeb.app
PORT = int(os.getenv("PORT", 8080))

# Command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your bot is running successfully.")

# Safety check
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing!")

# Create app
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))

# Define webhook path
webhook_path = f"/webhook/{BOT_TOKEN}"

# Start the webhook
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{APP_URL}{webhook_path}",
        webhook_path=webhook_path
    )
