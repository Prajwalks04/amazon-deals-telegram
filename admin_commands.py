from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils import is_admin, categories, save_admin_preference

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        await update.message.reply_text("You are not authorized to access admin panel.")
        return

    keyboard = [
        [InlineKeyboardButton(cat, callback_data=f"category_{cat}")]
        for cat in categories
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a category:", reply_markup=reply_markup)

async def handle_category_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    category = query.data.split("_", 1)[1]

    # Save category selection in context
    context.user_data["selected_category"] = category

    keyboard = [
        [InlineKeyboardButton("25% Off", callback_data="discount_25")],
        [InlineKeyboardButton("50% Off", callback_data="discount_50")],
        [InlineKeyboardButton("70% Off", callback_data="discount_70")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"Category selected: {category}\nNow choose a discount:", reply_markup=reply_markup)

async def handle_discount_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    discount = query.data.split("_", 1)[1]
    category = context.user_data.get("selected_category", "Unknown")

    await query.edit_message_text(f"Filters set:\nCategory: {category}\nDiscount: {discount}%\nDeals will be filtered accordingly.")

    # Save preferences (optional)
    await save_admin_preference(user_id=query.from_user.id, category=category, discount=discount)
