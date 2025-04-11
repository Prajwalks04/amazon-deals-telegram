import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from dotenv import load_dotenv
import requests

load_dotenv()

BOT_USERNAME = os.getenv("BOT_USERNAME", "PS_BOTz")
CHANNEL_LINK = os.getenv("CHANNEL_LINK", "https://t.me/ps_botz")
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "@PSBOTz")
GITHUB_URL = os.getenv("GITHUB_URL", "https://github.com/Prajwalks04/amazon-deals-telegram-bot")
DB_PROVIDER = os.getenv("DB_PROVIDER", "mongodb.com")
EXPLORE_MORE = os.getenv("EXPLORE_MORE", "https://t.me/trendyofferz")

async def send_welcome_message(update, context):
    welcome_image = open("assets/welcome.png", "rb")
    keyboard = [
        [
            InlineKeyboardButton("Source - GitHub", url=GITHUB_URL),
            InlineKeyboardButton("Main Channel", url=CHANNEL_LINK)
        ],
        [
            InlineKeyboardButton("Owner", url=f"https://t.me/{OWNER_USERNAME.strip('@')}"),
            InlineKeyboardButton("Explore More Deals", url=EXPLORE_MORE)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(
        photo=welcome_image,
        caption=f"**Welcome to {BOT_USERNAME}**\n\nMaintained by ChatGPT & Powered by OpenAI.\nFind latest deals, ₹1 offers, price drops, and more.\n\n**Main Channel**: {CHANNEL_LINK}\n**Database**: {DB_PROVIDER}",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=reply_markup
    )

async def send_deal_post(context: ContextTypes.DEFAULT_TYPE, chat_id, title, price, link, image_url, coupon_code=None, credit_offer=None, tags=None):
    caption = f"*{title}*\n\n"
    caption += f"💰 Price: ₹{price}\n"
    if coupon_code:
        caption += f"`Coupon: {coupon_code}`\n"
    if credit_offer:
        caption += f"💳 Offer: {credit_offer}\n"
    if tags:
        caption += "🏷️ " + ", ".join(tags) + "\n"
    caption += f"[Buy Now]({link})\n\n"
    caption += "_Limited time offer. Hurry!_"

    try:
        await context.bot.send_photo(
            chat_id=chat_id,
            photo=image_url,
            caption=caption,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        logging.error(f"Failed to send deal post: {e}")

def setup_webhook(application):
    from telegram.ext import Application
    import os

    webhook_url = os.getenv("WEBHOOK_URL")
    if webhook_url:
        application.run_webhook(
            listen="0.0.0.0",
            port=int(os.getenv("PORT", 8080)),
            webhook_url=webhook_url
        )
    else:
        raise ValueError("WEBHOOK_URL is not set in .env file")
