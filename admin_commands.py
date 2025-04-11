# admin_commands.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from utils import is_admin, categories, save_admin_preference

admin_only_commands = ['setting', 'status', 'channel', 'connects', 'users']

async def handle_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    command = update.message.text.lstrip('/')

    if not await is_admin(user_id):
        await update.message.reply_text("Access denied. Admins only.")
        return

    if command == 'setting':
        await show_category_buttons(update)
    elif command == 'status':
        await update.message.reply_text("Bot is running and connected.")
    elif command == 'channel':
        await update.message.reply_text("Main Channel: @ps_botz")
    elif command == 'connects':
        await update.message.reply_text("Connected to DB and Telegram API.")
    elif command == 'users':
        await update.message.reply_text("Tracking users & active sessions.")

async def show_category_buttons(update: Update):
    keyboard = [[InlineKeyboardButton(cat, callback_data=f"cat_{cat}")] for cat in categories]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose a category:", reply_markup=reply_markup)

async def handle_category_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    category = query.data.replace("cat_", "")
    context.user_data['selected_category'] = category

    discount_buttons = [
        [InlineKeyboardButton(f"{d}%", callback_data=f"disc_{d}")]
        for d in ["25", "50", "70", "90"]
    ]
    reply_markup = InlineKeyboardMarkup(discount_buttons)
    await query.edit_message_text(
        text=f"Selected Category: {category}\nNow select discount percentage:",
        reply_markup=reply_markup
    )

async def handle_discount_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    discount = query.data.replace("disc_", "")
    category = context.user_data.get('selected_category')

    await save_admin_preference(update.effective_user.id, category, discount)

    await query.edit_message_text(
        text=f"Preferences saved!\nCategory: {category}\nDiscount: {discount}%"
    )
# admin_commands.py placeholder for admin features
