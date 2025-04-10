# main.py placeholder import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")  # e.g. https://yourapp.koyeb.app

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Explore Deals", url="https://t.me/trendyofferz")],
        [InlineKeyboardButton("Main Channel", url="https://t.me/ps_botz")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_photo(
        photo="https://te.legra.ph/file/47c3742549e7b85eb1e53.jpg",  # Change to your logo
        caption=(
            "**Welcome to the Deal Hunter Bot!**\n\n"
            "Maintained by ChatGPT | Powered by OpenAI\n\n"
            "**Main Channel**: @ps_botz\n"
            "For more deals: @trendyofferz"
        ),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to explore deals. Stay tuned!")

# --- Main ---

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Set webhook
    webhook_url = f"{APP_URL}/{BOT_TOKEN}"
    application.run_webhook(
        listen="0.0.0.0",
        port=8080,
        webhook_url=webhook_url,
    )

if __name__ == "__main__":
    main()
 bot logic
