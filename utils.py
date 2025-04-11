from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("Source", url="https://github.com/Prajwalks04")],
        [InlineKeyboardButton("Owner", url="https://t.me/PSBOTz")],
        [InlineKeyboardButton("Database", url="https://www.mongodb.com/")],
        [InlineKeyboardButton("Main Channel", url="https://t.me/ps_botz")],
        [InlineKeyboardButton("Explore Deals", url="https://t.me/trendyofferz")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_admin_panel():
    keyboard = [
        [InlineKeyboardButton("Post Control", callback_data="admin_post")],
        [InlineKeyboardButton("Scheduling", callback_data="admin_schedule")],
        [InlineKeyboardButton("Manage Channels", callback_data="admin_channels")],
        [InlineKeyboardButton("User Access", callback_data="admin_users")],
        [InlineKeyboardButton("24/7 Posting", callback_data="admin_auto")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_category_keyboard():
    keyboard = [
        [InlineKeyboardButton("Clothes", callback_data="cat_clothes")],
        [InlineKeyboardButton("Accessories", callback_data="cat_accessories")],
        [InlineKeyboardButton("Electronics", callback_data="cat_electronics")],
        [InlineKeyboardButton("Kids", callback_data="cat_kids")],
        [InlineKeyboardButton("Search", callback_data="cat_search")]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_discount_keyboard():
    keyboard = [
        [InlineKeyboardButton("25%", callback_data="disc_25")],
        [InlineKeyboardButton("50%", callback_data="disc_50")],
        [InlineKeyboardButton("70%", callback_data="disc_70")],
        [InlineKeyboardButton("90%", callback_data="disc_90")]
    ]
    return InlineKeyboardMarkup(keyboard)
