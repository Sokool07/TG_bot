#!/usr/bin/env python3
"""
Скрипт для проверки конфигурации бота для Timeweb Cloud
"""

import os
import sys
from pathlib import Path

# Добавляем путь к модулям бота
sys.path.insert(0, str(Path(__file__).parent))

def check_required_env_vars():
    """Проверяет наличие обязательных переменных окружения"""
    required_vars = [
        'BOT_TOKEN',
        'CHANNEL_ID',
        'WEBHOOK_BASE_URL',
        'DB_HOST',
        'DB_USER',
        'DB_NAME',
        'REDIS_HOST'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Отсутствуют обязательные переменные окружения: {', '.join(missing_vars)}")
        return False
    else:
        print("✅ Все обязательные переменные окружения установлены")
        return True

def check_config_import():
    """Проверяет импорт конфигурации"""
    try:
        from bot.core.config import settings
        print("✅ Конфигурация успешно импортирована")
        
        # Проверяем основные настройки
        print(f"   - Webhook включен: {settings.USE_WEBHOOK}")
        print(f"   - Порт webhook: {settings.WEBHOOK_PORT}")
        print(f"   - Хост webhook: {settings.WEBHOOK_HOST}")
        print(f"   - Интеграции заглушки: {settings.INTEGRATIONS_STUB}")
        print(f"   - Аналитика отключена: {settings.AMPLITUDE_API_KEY is None}")
        
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта конфигурации: {e}")
        return False

def check_analytics_disabled():
    """Проверяет, что аналитика отключена"""
    try:
        from bot.services.analytics import analytics
        if analytics.logger is None:
            print("✅ Внешняя аналитика отключена")
            return True
        else:
            print("❌ Внешняя аналитика не отключена")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки аналитики: {e}")
        return False

def main():
    """Основная функция проверки"""
    print("🔍 Проверка конфигурации бота для Timeweb Cloud...")
    print("=" * 50)
    
    checks = [
        check_config_import,
        check_analytics_disabled,
        check_required_env_vars
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 Все проверки пройдены! Бот готов к развертыванию на Timeweb Cloud")
    else:
        print("⚠️  Некоторые проверки не пройдены. Проверьте конфигурацию.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
