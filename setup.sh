#!/bin/bash

# Telegram AI Image Bot - Quick Setup Script

echo "🤖 Telegram AI Image Bot - Quick Setup"
echo "======================================"

# Check Python version
python_version=$(python3 --version 2>&1)
echo "Python version: $python_version"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create data directories
echo "📁 Creating directories..."
mkdir -p data logs

# Copy environment file
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    echo "✏️ Please edit .env file with your configuration:"
    echo "   - TELEGRAM_BOT_TOKEN (required)"
    echo "   - OPENAI_API_KEY (required)"
    echo "   - Payment provider credentials (optional)"
    echo "   - ADMIN_USER_ID (recommended)"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "🚀 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Run: python run.py"
echo "   Or with Docker: docker-compose up -d"
echo ""
echo "📚 See README.md for detailed instructions"

