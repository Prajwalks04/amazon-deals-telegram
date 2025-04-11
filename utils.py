# utils.py

import os
from pymongo import MongoClient
from telegram.constants import ParseMode

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["amazon_bot"]
history_col = db["deal_history"]
admin_col = db["admins"]
prefs_col = db["admin_prefs"]

categories = ["Clothes", "Accessories", "Electronics", "Home", "Beauty"]

async def is_admin(user_id: int) -> bool:
    admin = admin_col.find_one({"user_id": user_id})
    return bool(admin)

async def save_admin_preference(user_id: int, category: str, discount: str):
    prefs_col.update_one(
        {"user_id": user_id},
        {"$set": {"category": category, "discount": discount}},
        upsert=True
    )

def already_posted(deal_id: str) -> bool:
    return history_col.find_one({"deal_id": deal_id}) is not None

def mark_as_posted(deal_id: str):
    history_col.insert_one({"deal_id": deal_id})

def format_price(price: float) -> str:
    return f"₹{int(price):,}"

def format_deal_message(title, price, original_price, link, coupon_code=None, labels=None):
    price_drop = original_price - price
    discount_percent = int((price_drop / original_price) * 100) if original_price else 0

    lines = [
        f"*{title}*",
        f"Price: *{format_price(price)}*  (was ~{format_price(original_price)}~)",
        f"Discount: *{discount_percent}%*"
    ]

    if labels:
        lines.append(" / ".join([f"`{label}`" for label in labels]))

    if coupon_code:
        lines.append(f"Coupon Code: `{coupon_code}`")

    lines.append(f"[Buy Now]({link})")

    if price <= 1:
        lines.append("⚠️ *₹1 Deal! Hurry!*")

    lines.append("_Limited Time Offer. Subject to stock._")

    return "\n".join(lines), ParseMode.MARKDOWN
# utils.py placeholder with helper functions
