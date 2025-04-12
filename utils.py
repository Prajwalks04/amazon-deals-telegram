import os
import asyncio
from pymongo import MongoClient
from telegram import InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
CHANNEL_ID = os.getenv("CHANNEL_ID")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client["telegram_deals"]
deals_collection = db["posted_deals"]

ADMIN_IDS = [int(admin.strip()) for admin in os.getenv("ADMIN_IDS", "").split(",") if admin.strip().isdigit()]


def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


def get_channel_id() -> str:
    return CHANNEL_ID


async def welcome_message(update, context):
    photo_path = "assets/logo.png"
    caption = (
        "<b>Welcome to the Best Deal Bot!</b>\n\n"
        "Find the latest trending deals, price drops, ₹1 offers, and more!\n\n"
        "<b>Maintained by ChatGPT | Powered by OpenAI</b>\n"
        "Explore more bots at @ps_botz\n\n"
        "<b>Main Channel:</b> @ps_botz\n<b>More Deals:</b> @trendyofferz"
    )

    buttons = [
        [
            InlineKeyboardButton("Source - GitHub", url="https://github.com/Prajwalks04"),
            InlineKeyboardButton("Owner - @PSBOTz", url="https://t.me/PSBOTz")
        ],
        [
            InlineKeyboardButton("Database - MongoDB", url="https://www.mongodb.com/"),
            InlineKeyboardButton("Main Channel - @ps_botz", url="https://t.me/ps_botz")
        ],
        [
            InlineKeyboardButton("Explore @trendyofferz", url="https://t.me/trendyofferz")
        ]
    ]

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=open(photo_path, 'rb'),
        caption=caption,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons)
    )


def has_been_posted(product_id: str) -> bool:
    return deals_collection.find_one({"product_id": product_id}) is not None


def mark_as_posted(product_id: str):
    deals_collection.insert_one({"product_id": product_id})


async def process_deal_posting(context: ContextTypes.DEFAULT_TYPE, deal: dict):
    product_id = deal.get("id")
    if has_been_posted(product_id):
        return

    title = deal.get("title", "No Title")
    price = deal.get("price", "")
    image_url = deal.get("image", "")
    url = deal.get("url", "")
    coupon = deal.get("coupon", "")
    credit_offer = deal.get("credit_offer", "")
    tags = deal.get("tags", [])

    is_one_rupee = "₹1" in price or price.strip() == "₹1"

    tag_text = " | ".join(tags)
    caption = f"<b>{title}</b>\n\nPrice: <b>{price}</b>\n\n"

    if coupon:
        caption += f"Coupon Code: <code>{coupon}</code>\n"
    if credit_offer:
        caption += f"Bank Offer: <code>{credit_offer}</code>\n"

    if is_one_rupee:
        caption += "\n<b>₹1 Deal Alert!</b> ⚡ Limited Stock! Buy Now!\n"

    if tag_text:
        caption += f"\nTags: {tag_text}"

    caption += f"\n\n<a href='{url}'>Buy Now</a>"

    message = await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=image_url,
        caption=caption,
        parse_mode=ParseMode.HTML
    )

    if is_one_rupee:
        await context.bot.pin_chat_message(chat_id=CHANNEL_ID, message_id=message.message_id)

    mark_as_posted(product_id)


async def send_1_rupee_alert(context: ContextTypes.DEFAULT_TYPE, deal: dict):
    title = deal.get("title", "₹1 Deal!")
    image_url = deal.get("image", "")
    url = deal.get("url", "")

    caption = (
        f"<b>₹1 Deal Alert!</b> ⚠️\n\n"
        f"<b>{title}</b>\n\n"
        f"<a href='{url}'>Buy Now</a>\n\n"
        "Limited Time Offer – Act Fast!"
    )

    message = await context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=image_url,
        caption=caption,
        parse_mode=ParseMode.HTML
    )

    await context.bot.pin_chat_message(chat_id=CHANNEL_ID, message_id=message.message_id)


async def check_for_deals_periodically(context: ContextTypes.DEFAULT_TYPE, fetch_deals_func):
    while True:
        try:
            deals = await fetch_deals_func()
            for deal in deals:
                await process_deal_posting(context, deal)
        except Exception as e:
            print(f"[Deal Check Error] {e}")
        await asyncio.sleep(600)  # every 10 minutes
