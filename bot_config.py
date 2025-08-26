# bot_config.py

import os

class BotConfig:
    def __init__(self):
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        self.FREE_CREDITS_PER_USER = int(os.getenv("FREE_CREDITS_PER_USER", 1))
        self.DATABASE_PATH = os.getenv("DATABASE_PATH", "bot_database.db")

# إنشاء كائن config لاستخدامه في run.py
config = BotConfig()
