import sqlite3
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

def debug_current_state():
    """Диагностика текущего состояния бота"""
    print("=== BOT DEBUG INFORMATION ===")
    
    # 1. Проверяем соединение с Telegram API
    print("\n1. Testing Telegram API connection...")
    try:
        response = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getMe", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                print(f"✅ Bot is alive: {data['result']['first_name']} (@{data['result']['username']})")
            else:
                print(f"❌ Bot error: {data}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
    except Exception as e:
        print(f"❌ Connection error: {e}")
    
    # 2. Проверяем базу данных
    print("\n2. Checking database...")
    try:
        conn = sqlite3.connect('bot.db')
        cursor = conn.cursor()
        
        # Проверяем таблицы
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"Tables in database: {tables}")
        
        # Количество записей
        cursor.execute("SELECT COUNT(*) FROM telegram_updates")
        count = cursor.fetchone()[0]
        print(f"Total updates in database: {count}")
        
        # Последний update_id
        cursor.execute("SELECT MAX(update_id) FROM telegram_updates")
        last_update = cursor.fetchone()[0]
        print(f"Last update_id in database: {last_update}")
        
        conn.close()
    except Exception as e:
        print(f"❌ Database error: {e}")
    
    # 3. Проверяем получение новых сообщений
    print("\n3. Checking for new messages from Telegram...")
    try:
        # Используем offset = last_update + 1
        offset = last_update + 1 if last_update else 0
        print(f"Requesting updates with offset: {offset}")
        
        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates",
            data={'offset': offset, 'timeout': 5},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                updates = data['result']
                print(f"📨 New updates available: {len(updates)}")
                
                for update in updates:
                    update_id = update['update_id']
                    message = update.get('message', {})
                    print(f"  - Update {update_id}: ", end="")
                    
                    if 'text' in message:
                        print(f"TEXT: '{message['text']}'")
                    elif 'photo' in message:
                        print(f"PHOTO: {len(message['photo'])} versions")
                    else:
                        print("OTHER")
            else:
                print(f"❌ Telegram API error: {data}")
        else:
            print(f"❌ HTTP error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error checking updates: {e}")

if __name__ == "__main__":
    debug_current_state()