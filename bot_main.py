# bot_main.py
import logging
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from bot_config import BotConfig

# إعداد اللوج
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# جلب التوكن من config
config = BotConfig()
TOKEN = config.TELEGRAM_BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا بوت تيليجرام الذكي 🤖")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"لقد كتبت: {text}")

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))
    
    # الرد على كل رسالة نصية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # تشغيل البوت
    logging.info("Bot is starting...")
    app.run_polling()

if __name__ == "__main__":
    run_bot()
