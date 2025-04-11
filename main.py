import logging
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv
import os
from utils import send_deal_post, send_welcome_message, setup_webhook
from admin_commands import admin_panel, handle_category_buttons, handle_discount_buttons

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = 8080
BASE_URL = os.getenv("BASE_URL")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Initialize the bot
app = Application.builder().token(TOKEN).build()

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_welcome_message(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to begin.\nFor admin: /setting, /status, /channel, /connects, /users")

# Health check endpoint
async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("OK")

# Add Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("setting", admin_panel))
app.add_handler(CommandHandler("status", admin_panel))
app.add_handler(CommandHandler("channel", admin_panel))
app.add_handler(CommandHandler("connects", admin_panel))
app.add_handler(CommandHandler("users", admin_panel))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_deal_post))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex("Clothes|Accessories|Electronics"), handle_category_buttons))
app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"\d+%"), handle_discount_buttons))

# Run the bot using webhook
if __name__ == "__main__":
    setup_webhook(app, BASE_URL, TOKEN, PORT)
