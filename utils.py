import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

ADMIN_IDS = os.getenv("ADMIN_IDS", "").split(",")  # comma-separated admin IDs

def is_admin(user_id: int) -> bool:
    return str(user_id) in ADMIN_IDS

def get_channel_id(update: Update) -> str:
    if update.effective_chat.type in ["channel", "supergroup", "group"]:
        return str(update.effective_chat.id)
    return ""

async def welcome_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Source - GitHub", url="https://github.com/Prajwalks04")],
        [InlineKeyboardButton("Owner - @PSBOTz", url="https://t.me/PSBOTz")],
        [InlineKeyboardButton("Database - MongoDB", url="https://www.mongodb.com/")],
        [InlineKeyboardButton("Main Channel - @ps_botz", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Explore Deals - @trendyofferz", url="https://t.me/trendyofferz")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://telegra.ph/file/79f52f689b75a93f12135.jpg",  # Replace with your welcome image
        caption=(
            "**Welcome to your Deal Bot!**\n\n"
            "This bot is maintained by ChatGPT and powered by OpenAI.\n"
            "Stay tuned for 24/7 trending deals.\n\n"
            "Follow @ps_botz for more bots like this!"
        ),
        parse_mode="Markdown",
        reply_markup=reply_markup
    )

def check_port() -> int:
    return int(os.getenv("PORT", 8080))
    
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Source", url="https://github.com/Prajwalks04")],
        [InlineKeyboardButton("Owner", url="https://t.me/PSBOTz")],
        [InlineKeyboardButton("Database", url="https://www.mongodb.com/")],
        [InlineKeyboardButton("Main Channel", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Explore Deals", url="https://t.me/trendyofferz")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_panel():
    keyboard = [
        [InlineKeyboardButton("Post Control", callback_data="admin_post")],
        [InlineKeyboardButton("Scheduling", callback_data="admin_schedule")],
        [InlineKeyboardButton("Manage Channels", callback_data="admin_channels")],
        [InlineKeyboardButton("User Access", callback_data="admin_users")],
        [InlineKeyboardButton("24/7 Posting", callback_data="admin_auto")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_category_keyboard():
    keyboard = [
        [InlineKeyboardButton("Clothes", callback_data="cat_clothes")],
        [InlineKeyboardButton("Accessories", callback_data="cat_accessories")],
        [InlineKeyboardButton("Electronics", callback_data="cat_electronics")],
        [InlineKeyboardButton("Kids", callback_data="cat_kids")],
        [InlineKeyboardButton("Search", callback_data="cat_search")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_discount_keyboard():
    keyboard = [
        [InlineKeyboardButton("25%", callback_data="disc_25")],
        [InlineKeyboardButton("50%", callback_data="disc_50")],
        [InlineKeyboardButton("70%", callback_data="disc_70")],
        [InlineKeyboardButton("90%", callback_data="disc_90")]
    ]
    return InlineKeyboardMarkup(keyboard)
