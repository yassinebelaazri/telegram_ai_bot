
# 🤖 Telegram AI Image Generator Bot

A complete Telegram bot that generates AI images using OpenAI DALL-E API with subscription management and multiple payment methods.

## ✨ Features

- 🎨 **AI Image Generation** - Uses OpenAI DALL-E 3 for high-quality image generation
- 💳 **Credit System** - 1 free credit for new users, 1 credit = 1 image
- 🌟 **Subscription Plans** - $5/month for unlimited image generation
- 💰 **Multiple Payment Methods** - PayPal, Stripe, Bitcoin (BTC), USDT
- 🛡️ **Content Filtering** - Blocks NSFW and harmful content
- 📊 **User Management** - SQLite database for user data and statistics
- 🔒 **Security** - Input validation and spam protection
- 📱 **User-Friendly** - Intuitive commands and inline keyboards

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- OpenAI API Key
- Payment provider accounts (optional)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd telegram_ai_bot
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run the bot**
```bash
python src/bot.py
```

## ⚙️ Configuration

### Required Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Bot Configuration
MONTHLY_SUBSCRIPTION_PRICE=5.00
FREE_CREDITS_PER_USER=1
DATABASE_PATH=bot_database.db
ADMIN_USER_ID=your_telegram_user_id_here
```

### Optional Payment Configuration

```env
# PayPal Configuration
PAYPAL_CLIENT_ID=your_paypal_client_id_here
PAYPAL_CLIENT_SECRET=your_paypal_client_secret_here
PAYPAL_MODE=sandbox  # or 'live' for production

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key_here
STRIPE_SECRET_KEY=your_stripe_secret_key_here

# Cryptocurrency Wallets
BTC_WALLET_ADDRESS=your_btc_wallet_address_here
USDT_WALLET_ADDRESS=your_usdt_wallet_address_here
```

## 📋 Setup Instructions

### 1. Create Telegram Bot

1. Message @BotFather on Telegram
2. Use `/newbot` command
3. Choose a name and username for your bot
4. Copy the bot token to your `.env` file

### 2. Get OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Create an account or sign in
3. Go to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

### 3. Setup Payment Methods (Optional)

#### PayPal
1. Create a PayPal Developer account
2. Create a new app in the PayPal Developer Dashboard
3. Get Client ID and Client Secret
4. Add them to your `.env` file

#### Stripe
1. Create a Stripe account
2. Get your API keys from the Stripe Dashboard
3. Add them to your `.env` file

#### Cryptocurrency
1. Create wallet addresses for BTC and USDT
2. Add the addresses to your `.env` file

### 4. Configure Admin Access

1. Get your Telegram user ID (you can use @userinfobot)
2. Add it to `ADMIN_USER_ID` in your `.env` file
3. This allows you to use the `/stats` command

## 🎯 Bot Commands

- `/start` - Start the bot and get welcome message
- `/help` - Show help information
- `/balance` - Check credit balance and subscription status
- `/subscribe` - View subscription options and payment methods
- `/stats` - Show bot statistics (admin only)

## 💡 Usage Examples

### Generate an Image
Simply send a text message to the bot:
```
A beautiful sunset over mountains with purple clouds
```

### Subscribe for Unlimited Access
Use the `/subscribe` command and choose your payment method.

## 🏗️ Project Structure

```
telegram_ai_bot/
├── src/
│   ├── bot.py              # Main bot application
│   ├── database.py         # Database operations
│   ├── image_generator.py  # OpenAI DALL-E integration
│   ├── payment_handler.py  # Payment processing
│   └── content_filter.py   # Content filtering
├── config/
│   └── config.py          # Configuration settings
├── docs/                  # Documentation
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 Customization

### Adding New Payment Methods

1. Extend the `PaymentHandler` class in `src/payment_handler.py`
2. Add new payment method to the bot's inline keyboard
3. Update the callback query handler

### Modifying Content Filter

Edit `src/content_filter.py` to:
- Add/remove banned words
- Modify filtering patterns
- Adjust sensitivity levels

### Changing Subscription Pricing

Update the `MONTHLY_SUBSCRIPTION_PRICE` in your `.env` file.

## 🚀 Deployment

### Using Docker (Recommended)

1. Create a Dockerfile:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "src/bot.py"]
```

2. Build and run:
```bash
docker build -t telegram-ai-bot .
docker run -d --env-file .env telegram-ai-bot
```

## 📊 Monitoring

### Logs
The bot logs important events to the console and can be configured to log to files.

### Statistics
Use the `/stats` command (admin only) to view:
- Total users
- Active subscribers
- Total images generated

## 🔒 Security Considerations

- Keep your API keys secure and never commit them to version control
- Use environment variables for all sensitive configuration
- Regularly update dependencies
- Monitor for unusual usage patterns
- Implement rate limiting for production use

## 🐛 Troubleshooting

### Common Issues

1. **Bot not responding**
   - Check if the bot token is correct
   - Verify internet connection
   - Check logs for error messages

2. **Image generation fails**
   - Verify OpenAI API key is valid
   - Check OpenAI account balance
   - Ensure content passes filtering

3. **Payment not working**
   - Verify payment provider credentials
   - Check webhook URLs are accessible
   - Review payment provider logs

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Happy bot building! 🚀**

