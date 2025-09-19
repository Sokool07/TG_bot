#!/usr/bin/env python3
"""
Простое тестовое приложение для проверки совместимости с Timeweb Cloud
Основано на примере Flask приложения от Timeweb Cloud
"""

from flask import Flask, jsonify
import os
import sys

app = Flask(__name__)

@app.route("/")
def hello():
    return "Timeweb Cloud + Docker + Telegram Bot = ❤️"

@app.route("/health")
def health():
    """Health check endpoint для Timeweb Cloud"""
    return jsonify({
        "status": "healthy",
        "service": "telegram-bot",
        "version": "1.0.0"
    })

@app.route("/webhook", methods=["POST"])
def webhook():
    """Webhook endpoint для Telegram бота"""
    return jsonify({"status": "webhook_ready"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"Starting test app on {host}:{port}")
    app.run(debug=False, host=host, port=port)
