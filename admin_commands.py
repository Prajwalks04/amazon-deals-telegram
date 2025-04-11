from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

ADMIN_IDS = ["your_admin_telegram_id_here"]  # Replace with actual admin ID(s)

async def handle_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("Access denied.")
        return

    keyboard = [
        [InlineKeyboardButton("Clothes", callback_data="category_clothes")],
        [InlineKeyboardButton("Accessories", callback_data="category_accessories")],
        [InlineKeyboardButton("Electronics", callback_data="category_electronics")],
        [InlineKeyboardButton("Kids", callback_data="category_kids")],
        [InlineKeyboardButton("Search", callback_data="search_feature")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a category:", reply_markup=reply_markup)

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_category = query.data.replace("category_", "")

    keyboard = [
        [InlineKeyboardButton("25% Off", callback_data="discount_25")],
        [InlineKeyboardButton("50% Off", callback_data="discount_50")],
        [InlineKeyboardButton("70% Off", callback_data="discount_70")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f"You selected *{selected_category.capitalize()}*. Now pick a discount:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def handle_discount_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_discount = query.data.replace("discount_", "")

    await query.edit_message_text(
        text=f"Great! You’ve selected *{selected_discount}%* deals.",
        parse_mode="Markdown"
    )

    # Here, you could log or store the selected filters (category + discount)
async def handle_search_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text="Please type the product name or keyword you want to search for."
    )

    # Set a flag in context.user_data to handle the next message as a search input
    context.user_data["awaiting_search_input"] = True
    
