import os
import requests
from pymongo import MongoClient
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode

# MongoDB setup
mongo_url = os.getenv("MONGO_DB_URI")
client = MongoClient(mongo_url)
db = client["amazon_deals"]
posted_deals = db["posted_deals"]
admin_prefs = db["admin_preferences"]

# Constants
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
CHANNEL_ID = os.getenv("CHANNEL_ID")
BASE_URL = os.getenv("BASE_URL")  # For webhook

categories = ["Clothes", "Accessories", "Electronics"]

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS

def save_admin_preference(user_id, category, discount):
    admin_prefs.update_one(
        {"user_id": user_id},
        {"$set": {"category": category, "discount": discount}},
        upsert=True
    )

def send_welcome_message(update, context):
    user = update.effective_user
    buttons = [
        [InlineKeyboardButton("Source - GitHub", url="https://github.com/Prajwalks04/amazon-deals-telegram-bot")],
        [InlineKeyboardButton("Main Channel - @ps_botz", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Explore More Deals - @trendyofferz", url="https://t.me/trendyofferz")]
    ]
    admin_buttons = []
    if is_admin(user.id):
        admin_buttons = [
            [InlineKeyboardButton("Admin Panel", callback_data="admin_panel")]
        ]
    update.message.reply_photo(
        photo=open("assets/welcome.jpg", "rb"),
        caption=(
            f"*Welcome to PS BOTz!*\n\n"
            "This bot delivers trending Amazon deals with coupons, discounts, and more.\n\n"
            "_Maintained by ChatGPT • Powered by OpenAI_\n\n"
            "*Join @ps_botz for updates!*"
        ),
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(buttons + admin_buttons)
    )

def send_deal_post(context, deal):
    deal_id = deal.get("id")
    if posted_deals.find_one({"id": deal_id}):
        return  # Avoid duplicates

    title = deal.get("title", "No Title")
    url = deal.get("url", "")
    image = deal.get("image", "")
    price = deal.get("price", "")
    original_price = deal.get("original_price", "")
    discount = deal.get("discount", "")
    coupon = deal.get("coupon", "")
    bank_offer = deal.get("bank_offer", "")
    urgency = ""

    if "₹1" in price:
        urgency = "*HURRY! ₹1 Deal!* "

    message = f"*{urgency}{title}*\n\n"
    message += f"💸 Price: ₹{price}\n"
    if original_price:
        message += f"❌ MRP: ₹{original_price}\n"
    if discount:
        message += f"✅ Discount: {discount}\n"
    if coupon:
        message += f"🎟 Coupon Code: `{coupon}`\n"
    if bank_offer:
        message += f"🏦 Bank Offer: {bank_offer}\n"
    message += f"\n🔗 [Buy Now]({url})\n\n"
    message += "_Limited Time Offer. Stay tuned for more!_"

    context.bot.send_photo(
        chat_id=CHANNEL_ID,
        photo=image,
        caption=message,
        parse_mode=ParseMode.MARKDOWN
    )

    posted_deals.insert_one({"id": deal_id})

def setup_webhook(app, bot):
    import telegram.ext.webhookhandler as wh
    from flask import request

    @app.route('/webhook', methods=['POST'])
    def webhook():
        if request.method == "POST":
            update = telegram.Update.de_json(request.get_json(force=True), bot)
            bot.update_queue.put(update)
            return "ok"

    bot.set_webhook(f"{BASE_URL}/webhook")

def get_admin_preferences(user_id):
    return admin_prefs.find_one({"user_id": user_id})
