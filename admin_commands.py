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
