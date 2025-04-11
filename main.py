import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from utils import get_channel_id, is_admin, welcome_message
from admin_commands import handle_admin_command, handle_category_selection, handle_discount_selection

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_URL = os.getenv("APP_URL")
PORT = int(os.getenv("PORT", 8080))

# Basic start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if update.message:
        await update.message.reply_photo(
            photo="https://telegra.ph/file/b68f1b8761b46b2a77f5e.jpg",  # Your welcome image URL
            caption=welcome_message(),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Source - GitHub", url="https://github.com/Prajwalks04")],
                [InlineKeyboardButton("Main Channel - @ps_botz", url="https://t.me/ps_botz")],
                [InlineKeyboardButton("Explore Deals - @trendyofferz", url="https://t.me/trendyofferz")],
                [InlineKeyboardButton("Owner - @PSBOTz", url="https://t.me/PSBOTz")],
                [InlineKeyboardButton("Admin Panel", callback_data="admin") if await is_admin(user_id) else None],
            ])
        )

# Help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Show welcome message\n"
        "/help - Show this help text\n"
        "/id - Get your Telegram ID\n"
        "/channel - Show linked channel\n"
        "/setting - (Admins only) Configure filters and settings"
    )

# ID command
async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your ID: `{update.effective_user.id}`", parse_mode="Markdown")

# Channel command
async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    channel_id = get_channel_id()
    await update.message.reply_text(f"Connected channel: `{channel_id}`", parse_mode="Markdown")
