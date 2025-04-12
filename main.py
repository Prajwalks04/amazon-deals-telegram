import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from utils import check_for_deals_periodically, send_1_rupee_alert
from admin_commands import handle_admin_command

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "8080"))
APP_URL = os.getenv("APP_URL")  # e.g., https://your-koyeb-app.koyeb.app

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

WELCOME_IMG = "https://envs.sh/GVs.jpg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Source - GitHub", url="https://github.com/Prajwalks04/amazon-deals-telegram")],
        [InlineKeyboardButton("Owner - @PSBOTz", url="https://t.me/PSBOTz")],
        [InlineKeyboardButton("Main Channel - @ps_botz", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Explore More Deals", url="https://t.me/trendyofferz")],
    ]

    admin_keyboard = [
        [InlineKeyboardButton("Admin Panel", callback_data="admin_panel")]
    ]

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=WELCOME_IMG,
        caption=(
            "<b>Welcome to Amazon Deals Bot!</b>\n\n"
            "Find the latest trending deals, ₹1 offers, contests, and more!\n\n"
            "Maintained by ChatGPT | Powered by OpenAI\n"
            "Checkout @ps_botz for more bots like this."
        ),
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard + admin_keyboard),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Use /start to begin. Stay tuned for amazing offers!")

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "admin_panel":
        buttons = [
            [InlineKeyboardButton("Status", callback_data="status")],
            [InlineKeyboardButton("Settings", callback_data="setting")],
            [InlineKeyboardButton("Users", callback_data="users")],
            [InlineKeyboardButton("Channel", callback_data="channel")],
            [InlineKeyboardButton("Connects", callback_data="connects")],
            [InlineKeyboardButton("Search", switch_inline_query_current_chat="")],
        ]
        await query.edit_message_text(
            "<b>Admin Control Panel</b>",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await handle_admin_command(update, context)

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is healthy and running!")

def main():
    if not BOT_TOKEN or not APP_URL:
        raise ValueError("BOT_TOKEN or APP_URL is missing from environment variables.")

    application = Application.builder().token(BOT_TOKEN).build()

    # Webhook setup
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=f"{APP_URL}/webhook",
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("health", health_check))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_admin_command))
    application.add_handler(CallbackQueryHandler(handle_callback_query))

    # Start background tasks
    asyncio.create_task(check_for_deals_periodically(application.bot))
    asyncio.create_task(send_1_rupee_alert(application.bot))

    application.run_polling()

if __name__ == "__main__":
    main()
