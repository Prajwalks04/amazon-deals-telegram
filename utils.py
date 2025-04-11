import os
import requests
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.constants import ParseMode

load_dotenv()

BOT_NAME = "PS BOTz"
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@ps_botz")
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()]

categories = ["Clothes", "Accessories", "Electronics"]
admin_preferences = {}

def is_admin(user_id):
    return user_id in ADMIN_IDS

def save_admin_preference(user_id, preference_type, value):
    if user_id not in admin_preferences:
        admin_preferences[user_id] = {}
    admin_preferences[user_id][preference_type] = value

def get_admin_preference(user_id):
    return admin_preferences.get(user_id, {})

def send_welcome_message(bot, chat_id):
    buttons = [
        [InlineKeyboardButton("Source - GitHub", url="https://github.com/Prajwalks04")],
        [InlineKeyboardButton("Owner - @PSBOTz", url="https://t.me/PSBOTz")],
        [InlineKeyboardButton("Main Channel", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Explore Deals", url="https://t.me/trendyofferz")]
    ]
    welcome_text = (
        f"**Welcome to {BOT_NAME}**\n\n"
        "Maintained by ChatGPT and powered by OpenAI.\n"
        "Discover top deals, coupons, and more!"
    )
    bot.send_photo(
        chat_id=chat_id,
        photo="https://telegra.ph/file/3bb75c795b790dd8dc2cf.jpg",  # Or your hosted banner
        caption=welcome_text,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def send_deal_post(bot, chat_id, title, link, price, image_url, coupon=None, extra_note=None):
    message = f"*{title}*\n\n"
    message += f"Price: ₹{price}\n"
    if coupon:
        message += f"Coupon Code: `{coupon}`\n"
    if extra_note:
        message += f"{extra_note}\n"
    message += f"[Buy Now]({link})"

    bot.send_photo(
        chat_id=chat_id,
        photo=image_url,
        caption=message,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
    )

def setup_webhook(bot, webhook_url):
    bot.delete_webhook()
    bot.set_webhook(url=webhook_url)
