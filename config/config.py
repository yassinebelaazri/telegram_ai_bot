
"""
Configuration module for Telegram AI Bot
Centralized configuration management
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BotConfig:
    """Bot configuration class"""
    
    # Telegram Bot Settings
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'dall-e-3')
    OPENAI_IMAGE_SIZE = os.getenv('OPENAI_IMAGE_SIZE', '1024x1024')
    OPENAI_IMAGE_QUALITY = os.getenv('OPENAI_IMAGE_QUALITY', 'standard')
    OPENAI_IMAGE_STYLE = os.getenv('OPENAI_IMAGE_STYLE', 'vivid')
    
    # Database Settings
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'bot_database.db')
    
    # Bot Business Logic
    MONTHLY_SUBSCRIPTION_PRICE = float(os.getenv('MONTHLY_SUBSCRIPTION_PRICE', '5.00'))
    FREE_CREDITS_PER_USER = int(os.getenv('FREE_CREDITS_PER_USER', '1'))
    MAX_PROMPT_LENGTH = int(os.getenv('MAX_PROMPT_LENGTH', '1000'))
    MIN_PROMPT_LENGTH = int(os.getenv('MIN_PROMPT_LENGTH', '3'))
    
    # Admin Settings
    ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))
    
    # Payment Settings
    PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
    PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
    PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')
    
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
    
    BTC_WALLET_ADDRESS = os.getenv('BTC_WALLET_ADDRESS')
    USDT_WALLET_ADDRESS = os.getenv('USDT_WALLET_ADDRESS')
    
    # Logging Settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'bot.log')
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        errors = []
        warnings = []
        
        # Required settings
        if not cls.TELEGRAM_BOT_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN is required")
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
        
        # Optional but recommended settings
        if not cls.ADMIN_USER_ID:
            warnings.append("ADMIN_USER_ID not set - admin features will be disabled")
        
        # Payment method validation
        payment_methods = []
        if cls.PAYPAL_CLIENT_ID and cls.PAYPAL_CLIENT_SECRET:
            payment_methods.append("PayPal")
        
        if cls.STRIPE_SECRET_KEY:
            payment_methods.append("Stripe")
        
        if cls.BTC_WALLET_ADDRESS:
            payment_methods.append("Bitcoin")
        
        if cls.USDT_WALLET_ADDRESS:
            payment_methods.append("USDT")
        
        if not payment_methods:
            warnings.append("No payment methods configured")
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'payment_methods': payment_methods
        }

# Create global config instance
config = BotConfig()

