#!/usr/bin/env python3
"""
Quick start script for Telegram AI Image Bot
This script validates configuration and starts the bot
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from config.config import config

def main():
    """Main entry point"""
    print("🤖 Telegram AI Image Generator Bot")
    print("=" * 50)
    
    # Validate configuration
    validation = config.validate_config()
    print(config.get_config_summary())
    
    if not validation['valid']:
        print("\n❌ Cannot start bot due to configuration errors.")
        print("Please fix the errors above and try again.")
        sys.exit(1)
    
    if validation['warnings']:
        print("\n⚠️ Starting with warnings. Some features may be limited.")
        input("Press Enter to continue or Ctrl+C to abort...")
    
    print("\n🚀 Starting bot...")
    
    try:
        from bot import TelegramAIBot
        bot = TelegramAIBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

