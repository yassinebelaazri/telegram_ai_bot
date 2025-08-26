
"""
Payment Handler module for Telegram AI Bot
Handles payment processing via PayPal, Stripe, and Cryptocurrency
"""

import os
import logging
import uuid
import hashlib
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class PaymentHandler:
    def __init__(self):
        """Initialize payment handler with API credentials"""
        # PayPal credentials
        self.paypal_client_id = os.getenv('PAYPAL_CLIENT_ID')
        self.paypal_client_secret = os.getenv('PAYPAL_CLIENT_SECRET')
        self.paypal_mode = os.getenv('PAYPAL_MODE', 'sandbox')  # 'sandbox' or 'live'
        
        # Stripe credentials
        self.stripe_publishable_key = os.getenv('STRIPE_PUBLISHABLE_KEY')
        self.stripe_secret_key = os.getenv('STRIPE_SECRET_KEY')
        
        # Crypto wallet addresses
        self.btc_wallet = os.getenv('BTC_WALLET_ADDRESS')
        self.usdt_wallet = os.getenv('USDT_WALLET_ADDRESS')
        
        logger.info("Payment handler initialized")
    
    def create_payment_link(self, user_id: int, amount: float, payment_method: str) -> Optional[Dict[str, Any]]:
        """
        Create payment link based on the selected method
        
        Args:
            user_id (int): Telegram user ID
            amount (float): Payment amount in USD
            payment_method (str): Payment method ('paypal', 'stripe', 'btc', 'usdt')
            
        Returns:
            Optional[Dict[str, Any]]: Payment information or None if failed
        """
        try:
            if payment_method == 'paypal':
                return self._create_paypal_payment(user_id, amount)
            elif payment_method == 'stripe':
                return self._create_stripe_payment(user_id, amount)
            elif payment_method == 'btc':
                return self._create_crypto_payment(user_id, amount, 'BTC')
            elif payment_method == 'usdt':
                return self._create_crypto_payment(user_id, amount, 'USDT')
            else:
                logger.error(f"Unsupported payment method: {payment_method}")
                return None
                
        except Exception as e:
            logger.error(f"Error creating payment link: {e}")
            return None
    
    def _create_paypal_payment(self, user_id: int, amount: float) -> Optional[Dict[str, Any]]:
        """Create PayPal payment link"""
        if not self.paypal_client_id or not self.paypal_client_secret:
            logger.error("PayPal credentials not configured")
            return None
        
        try:
            transaction_id = f"paypal_{user_id}_{int(datetime.now().timestamp())}"
            base_url = "https://www.sandbox.paypal.com" if self.paypal_mode == 'sandbox' else "https://www.paypal.com"
            
            payment_url = (
                f"{base_url}/cgi-bin/webscr?"
                f"cmd=_xclick&"
                f"business={self.paypal_client_id}&"
                f"item_name=AI Image Bot Premium Subscription&"
                f"amount={amount}&"
                f"currency_code=USD&"
                f"custom={transaction_id}"
            )
            
            return {
                'payment_url': payment_url,
                'transaction_id': transaction_id,
                'method': 'paypal',
                'amount': amount,
                'currency': 'USD'
            }
            
        except Exception as e:
            logger.error(f"Error creating PayPal payment: {e}")
            return None
    
    def _create_stripe_payment(self, user_id: int, amount: float) -> Optional[Dict[str, Any]]:
        """Create Stripe payment link"""
        if not self.stripe_secret_key:
            logger.error("Stripe credentials not configured")
            return None
        
        try:
            transaction_id = f"stripe_{user_id}_{int(datetime.now().timestamp())}"
            payment_url = f"https://checkout.stripe.com/pay/{transaction_id}"
            
            return {
                'payment_url': payment_url,
                'transaction_id': transaction_id,
                'method': 'stripe',
                'amount': amount,
                'currency': 'USD'
            }
            
        except Exception as e:
            logger.error(f"Error creating Stripe payment: {e}")
            return None
    
    def _create_crypto_payment(self, user_id: int, amount: float, crypto_type: str) -> Optional[Dict[str, Any]]:
        """Create cryptocurrency payment instructions"""
        try:
            if crypto_type == 'BTC':
                wallet_address = self.btc_wallet
            elif crypto_type == 'USDT':
                wallet_address = self.usdt_wallet
            else:
                logger.error(f"Unsupported crypto type: {crypto_type}")
                return None
            
            if not wallet_address:
                logger.error(f"{crypto_type} wallet address not configured")
                return None
            
            reference = self._generate_payment_reference(user_id, crypto_type)
            
            return {
                'wallet_address': wallet_address,
                'reference': reference,
                'amount_usd': amount,
                'crypto_type': crypto_type,
                'method': crypto_type.lower()
            }
            
        except Exception as e:
            logger.error(f"Error creating crypto payment: {e}")
            return None
    
    def _generate_payment_reference(self, user_id: int, crypto_type: str) -> str:
        """Generate unique payment reference for crypto transactions"""
        timestamp = int(datetime.now().timestamp())
        raw_string = f"{user_id}_{crypto_type}_{timestamp}"
        reference = hashlib.md5(raw_string.encode()).hexdigest()[:12].upper()
        return f"AIBOT-{reference}"

