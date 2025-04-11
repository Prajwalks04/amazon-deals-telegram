from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, CommandHandler
from utils import is_admin

# Admin command: /setting
async def setting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update):
        return

    keyboard = [
        [InlineKeyboardButton("Clothes", callback_data="cat_clothes"),
         InlineKeyboardButton("Accessories", callback_data="cat_accessories")],
        [InlineKeyboardButton("Electronics", callback_data="cat_electronics"),
         InlineKeyboardButton("Kids", callback_data="cat_kids")],
        [InlineKeyboardButton("Search", switch_inline_query_current_chat="")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a category:", reply_markup=reply_markup)
async def category_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.split("_")[1]
    context.user_data["category"] = category

    keyboard = [
        [InlineKeyboardButton("25%", callback_data="discount_25"),
         InlineKeyboardButton("50%", callback_data="discount_50")],
        [InlineKeyboardButton("70%", callback_data="discount_70"),
         InlineKeyboardButton("90%", callback_data="discount_90")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(f"Selected category: {category.capitalize()}\nNow choose a discount:",
                                  reply_markup=reply_markup)
    async def discount_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async def handle_discount_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_discount = query.data

    await query.edit_message_text(
        text=f"Great! You've selected {selected_discount}% off deals in this category."
    )

    # You can now store selected category + discount for future filtering logic
    
    query = update.callback_query
    await query.answer()

    discount = query.data.split("_")[1]
    context.user_data["discount"] = discount

    category = context.user_data.get("category", "Not selected")
    await query.edit_message_text(
        f"Filter set!\n\nCategory: *{category.capitalize()}*\nDiscount: *{discount}%*",
        parse_mode=constants.ParseMode.MARKDOWN
    )
    
