# main.py

import os
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters
)
from dotenv import load_dotenv
from utils import send_welcome_message, fetch_and_post_deals
from admin_commands import register_admin_handlers

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Example: https://your-koyeb-app.koyeb.app/webhook
PORT = int(os.getenv("PORT", 8080))

# Initialize bot app
app = ApplicationBuilder().token(TOKEN).build()

# Command handlers
@app.command_handler("start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_welcome_message(update, context)

@app.command_handler("help")
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This bot posts trending deals 24/7 from Amazon.\nUse /settings if you're an admin.")

# Add custom admin commands
register_admin_handlers(app)

# Default message handler
@app.message_handler(filters.TEXT & ~filters.COMMAND)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Please use a command or wait for trending deals.")

# Health check endpoint
async def health_check(request):
    return web.Response(text="Bot is healthy")

# Webhook handler
async def handle_webhook(request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.update_queue.put(update)
    return web.Response(text="OK")

# Main runner
async def main():
    runner = web.AppRunner(web.Application())
    runner.app.router.add_post("/webhook", handle_webhook)
    runner.app.router.add_get("/", health_check)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()

    # Set webhook URL
    await app.bot.set_webhook(url=WEBHOOK_URL + "/webhook")

    print("Bot is running with webhook...")
    await app.run_polling(close_loop=False)  # Runs update queue manually

if __name__ == "__main__":
    asyncio.run(main())
