import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from utils import send_deal_post, send_welcome_message, setup_webhook
from admin_commands import handle_category_buttons, handle_discount_buttons

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

print(f"Loaded BOT_TOKEN: {BOT_TOKEN}")

# Basic commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_welcome_message(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send /start to begin. Use admin commands to manage deals.")

# Register command and callback handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CallbackQueryHandler(handle_category_buttons, pattern="^category_"))
app.add_handler(CallbackQueryHandler(handle_discount_buttons, pattern="^discount_"))

# Webhook setup (for Koyeb)
@app.get("/")
async def root(request):
    return "Bot is alive"

if __name__ == "__main__":
    setup_webhook(app)
