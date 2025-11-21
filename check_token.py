import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('BOT_TOKEN')

print("=== ПРОВЕРКА ТОКЕНА ===")
print(f"Токен загружен: {'ДА' if token else 'НЕТ'}")
print(f"Длина токена: {len(token) if token else 0}")

if token:
    print(f"Первые 10 символов: {token[:10]}...")
    print(f"Последние 10 символов: ...{token[-10:]}")
    
    # Проверяем формат токена
    if ':' in token:
        print("✅ Формат токена правильный (содержит ':')")
        bot_id, token_part = token.split(':', 1)
        print(f"Bot ID: {bot_id}")
    else:
        print("❌ Неправильный формат токена (должен содержать ':')")
else:
    print("❌ Токен не найден в .env файле")