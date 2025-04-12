import os
import asyncio
import logging
from pymongo import MongoClient
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure
import signal

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
CHANNEL_ID = os.getenv("CHANNEL_ID")
DEAL_CHECK_INTERVAL = int(os.getenv("DEAL_CHECK_INTERVAL", "600"))  # default 10 minutes

# Ensure environment variables are set
if not MONGO_URI or not CHANNEL_ID:
    raise EnvironmentError("Missing necessary environment variables: MONGO_URI or CHANNEL_ID.")

# Connect to MongoDB with exception handling
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client["telegram_deals"]
    deals_collection = db["posted_deals"]
except ConnectionFailure as e:
    logging.error(f"Database connection failed: {e}")
    raise

# Graceful shutdown handler
def shutdown_handler(signum, frame):
    logging.info("Shutting down gracefully...")
    mongo_client.close()  # Close MongoDB connection
    exit(0)

# Register signal handler for graceful shutdown
signal.signal(signal.SIGINT, shutdown_handler)  # Handle Ctrl+C

# MongoDB functions to check if a deal has been posted
def has_been_posted(product_id: str) -> bool:
    return deals_collection.find_one({"product_id": product_id}) is not None

def mark_as_posted(product_id: str):
    deals_collection.insert_one({"product_id": product_id})

# Posting quiz and event updates
async def post_quiz_and_event_updates(context: ContextTypes.DEFAULT_TYPE, deal: dict):
    if "quiz" in deal.get("tags", []):
        title = deal.get("title", "No Title")
        image_url = deal.get("image", "")
        url = deal.get("url", "")

        caption = (
            f"<b>{title}</b>\n\n"
            f"Don't miss out on this Quiz/Event!\n\n"
            f"<a href='{url}'>Join Now</a>\n\n"
            "Hurry, limited spots available!"
        )

        message = await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=image_url,
            caption=caption,
            parse_mode=ParseMode.HTML
        )

        await context.bot.pin_chat_message(chat_id=CHANNEL_ID, message_id=message.message_id)

# Processing deals before posting them
async def process_deal_posting(context: ContextTypes.DEFAULT_TYPE, deal: dict):
    product_id = deal.get("id")
    if has_been_posted(product_id):
        return

    title = deal.get("title", "No Title")
    price = deal.get("price", "No Price")
    image_url = deal.get("image", "default_image.jpg")
    url = deal.get("url", "#")
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
    await post_quiz_and_event_updates(context, deal)

# Periodically check for new deals
async def check_for_deals_periodically(bot):
    from fetch_deals import fetch_trending_deals  # Make sure this file exists

    class DummyContext:
        def __init__(self, bot):
            self.bot = bot

    while True:
        try:
            deals = await fetch_trending_deals()
            for deal in deals:
                await process_deal_posting(DummyContext(bot), deal)
        except Exception as e:
            logging.error(f"[Deal Check Error] {e}")
        await asyncio.sleep(DEAL_CHECK_INTERVAL)

# Sending ₹1 deal alert
async def send_1_rupee_alert(bot):
    alert_text = (
        "<b>₹1 Deal Alert!</b>\n\n"
        "Stay tuned for exciting ₹1 flash deals coming soon!\n\n"
        "We’ll post the moment a ₹1 product is live!\n\n"
        "#OneRupee #FlashDeal #ps_botz"
    )
    await bot.send_message(chat_id=CHANNEL_ID, text=alert_text, parse_mode=ParseMode.HTML)
