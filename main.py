import os
import logging
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from telegram.ext import (
    Application,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
)
from utils import (
    is_admin,
    welcome_message,
    process_deal_posting,
    check_for_deals_periodically,
    send_1_rupee_alert,
    post_quiz_and_event_updates,
)
from admin_commands import (
    handle_admin_command,
    handle_category_selection,
    handle_discount_selection,
    handle_search_button,
)

load_dotenv()

# Logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Environment Variables
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8080))

# Bot Commands
COMMANDS = [
    BotCommand("start", "Start the bot"),
    BotCommand("help", "Get help"),
    BotCommand("id", "Get your chat ID"),
    BotCommand("channel", "Show configured channel"),
    BotCommand("setting", "Bot settings (admin only)"),
    BotCommand("status", "Bot status (admin only)"),
    BotCommand("connects", "Show linked groups/channels"),
    BotCommand("users", "Show total users"),
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await welcome_message(update, context)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This bot shares Amazon trending deals 24/7.")


async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your Chat ID: `{update.effective_chat.id}`", parse_mode="Markdown")


async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel = os.getenv("TELEGRAM_CHANNEL_ID", "Not configured")
    await update.message.reply_text(f"Deals are posted to: `{channel}`", parse_mode="Markdown")


async def health_check(request):
    return "OK", 200


def main():
    app = Application.builder().token(TOKEN).build()

    # Register Bot Commands
    asyncio.run(app.bot.set_my_commands(COMMANDS))

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("id", id_command))
    app.add_handler(CommandHandler("channel", channel_command))
    app.add_handler(CommandHandler(["setting", "status", "connects", "users"], handle_admin_command))
    app.add_handler(CallbackQueryHandler(handle_category_selection, pattern="^category_"))
    app.add_handler(CallbackQueryHandler(handle_discount_selection, pattern="^discount_"))
    app.add_handler(CallbackQueryHandler(handle_search_button, pattern="^search_deals$"))

    # Background tasks
    app.job_queue.run_repeating(check_for_deals_periodically, interval=600, first=5)
    app.job_queue.run_repeating(send_1_rupee_alert, interval=300, first=10)
    app.job_queue.run_repeating(post_quiz_and_event_updates, interval=1800, first=30)

    # Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        health_check_path="/",
        allowed_updates=Update.ALL_TYPES,
    )


if __name__ == "__main__":
    main()
