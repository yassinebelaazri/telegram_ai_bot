# run.py

from bot_config import BotConfig
from bot_main import TelegramBot

def main():
    # إنشاء كائن التكوين
    config = BotConfig()

    # -----------------------------------------------
    # تم التعليق على السطر الذي يسبب الخطأ
    # print(config.get_config_summary())
    # -----------------------------------------------

    # تشغيل البوت
    bot = TelegramBot(config)
    bot.run()

if __name__ == "__main__":
    main()
