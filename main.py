import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Load .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # Your Koyeb URL (without https://)
PORT = int(os.getenv("PORT", 8080))  # Fallback to 8080 if not set

# Basic start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Your bot is running successfully.")

# Check if BOT_TOKEN is valid
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing! Check your .env or Koyeb environment variables.")

# Build and run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add command handlers
app.add_handler(CommandHandler("start", start))

# Run the bot using webhook
if __name__ == "__main__":
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"https://{APP_URL}/webhook/{BOT_TOKEN}"
    )
