
"""
Database module for Telegram AI Image Bot
Handles user management, credits, and subscriptions
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class BotDatabase:
    def __init__(self, db_path: str = "bot_database.db"):
        """Initialize database connection and create tables"""
        self.db_path = db_path
        self.init_database()
        
    def init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                credits INTEGER DEFAULT 1,
                is_subscribed BOOLEAN DEFAULT FALSE,
                subscription_end_date TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_active TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Image generation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                prompt TEXT,
                image_url TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Payment transactions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                currency TEXT,
                payment_method TEXT,
                transaction_id TEXT,
                status TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully")
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user information by user_id"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return dict(user)
        return None
    
    def create_user(self, user_id: int, username: str = None, 
                   first_name: str = None, last_name: str = None) -> bool:
        """Create a new user with free credits"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (user_id, username, first_name, last_name, credits)
                VALUES (?, ?, ?, ?, 1)
            ''', (user_id, username, first_name, last_name))
            conn.commit()
            conn.close()
            logging.info(f"New user created: {user_id}")
            return True
        except sqlite3.IntegrityError:
            conn.close()
            logging.warning(f"User {user_id} already exists")
            return False
    
    def update_user_activity(self, user_id: int):
        """Update user's last activity timestamp"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET last_active = CURRENT_TIMESTAMP 
            WHERE user_id = ?
        ''', (user_id,))
        conn.commit()
        conn.close()
    
    def get_user_credits(self, user_id: int) -> int:
        """Get user's current credit balance"""
        user = self.get_user(user_id)
        if user:
            return user['credits']
        return 0
    
    def deduct_credit(self, user_id: int) -> bool:
        """Deduct one credit from user's balance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if user has credits
        cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result and result[0] > 0:
            cursor.execute('''
                UPDATE users SET credits = credits - 1 
                WHERE user_id = ?
            ''', (user_id,))
            conn.commit()
            conn.close()
            return True
        
        conn.close()
        return False
    
    def add_credits(self, user_id: int, credits: int) -> bool:
        """Add credits to user's balance"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET credits = credits + ? 
            WHERE user_id = ?
        ''', (credits, user_id))
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return affected_rows > 0
    
    def is_user_subscribed(self, user_id: int) -> bool:
        """Check if user has active subscription"""
        user = self.get_user(user_id)
        if not user or not user['is_subscribed']:
            return False
        
        if user['subscription_end_date']:
            end_date = datetime.fromisoformat(user['subscription_end_date'])
            return datetime.now() < end_date
        
        return False
    
    def activate_subscription(self, user_id: int, duration_days: int = 30) -> bool:
        """Activate subscription for user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        end_date = datetime.now() + timedelta(days=duration_days)
        
        cursor.execute('''
            UPDATE users 
            SET is_subscribed = TRUE, subscription_end_date = ?
            WHERE user_id = ?
        ''', (end_date.isoformat(), user_id))
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        if affected_rows > 0:
            logging.info(f"Subscription activated for user {user_id}")
            return True
        return False
    
    def save_image_generation(self, user_id: int, prompt: str, image_url: str):
        """Save image generation history"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO image_history (user_id, prompt, image_url)
            VALUES (?, ?, ?)
        ''', (user_id, prompt, image_url))
        
        conn.commit()
        conn.close()
        logging.info(f"Image generation saved for user {user_id}")
    
    def save_transaction(self, user_id: int, amount: float, currency: str,
                        payment_method: str, transaction_id: str, status: str):
        """Save payment transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transactions 
            (user_id, amount, currency, payment_method, transaction_id, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, amount, currency, payment_method, transaction_id, status))
        
        conn.commit()
        conn.close()
        logging.info(f"Transaction saved for user {user_id}: {status}")
    
    def get_user_stats(self) -> Dict[str, int]:
        """Get general statistics about users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Active subscribers
        cursor.execute('''
            SELECT COUNT(*) FROM users 
            WHERE is_subscribed = TRUE AND subscription_end_date > datetime('now')
        ''')
        active_subscribers = cursor.fetchone()[0]
        
        # Total images generated
        cursor.execute("SELECT COUNT(*) FROM image_history")
        total_images = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_users': total_users,
            'active_subscribers': active_subscribers,
            'total_images': total_images
        }

