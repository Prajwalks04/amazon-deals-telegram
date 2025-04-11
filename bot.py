from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import re

# Format and send a deal message
async def send_deal_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Dummy filter for test purposes
    if "₹" not in text:
        await update.message.reply_text("Invalid deal format. Please include ₹ price.")
        return

    price_match = re.search(r"₹\s?(\d+)", text)
    price = int(price_match.group(1)) if price_match else 0

    is_1_rupee = price == 1
    message = f"<b>🔥 Hot Deal 🔥</b>\n\n{text}"

    if is_1_rupee:
        message = f"⚠️ <b>₹1 Loot Deal</b> ⚠️\n⏳ Limited stock. Buy Now!\n\n" + message

    if "Coupon:" in text:
        message = re.sub(r"Coupon:\s?([A-Z0-9]+)", r"<code>\1</code>", message)

    if "Credit Card" in text:
        message += "\n💳 Extra discount on Credit Card"

    buttons = [
        [InlineKeyboardButton("Buy Now", url="https://www.amazon.in/")],
        [InlineKeyboardButton("Explore More Deals", url="https://t.me/trendyofferz")]
    ]

    await update.message.reply_html(message, reply_markup=InlineKeyboardMarkup(buttons))
