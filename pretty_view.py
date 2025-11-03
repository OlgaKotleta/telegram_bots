import sqlite3
import json
from datetime import datetime

def pretty_view_updates():
    """Красивый просмотр telegram_updates"""
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    
    # Получаем все записи
    cursor.execute('''
        SELECT id, update_id, update_data, timestamp 
        FROM telegram_updates 
        ORDER BY timestamp DESC
    ''')
    
    updates = cursor.fetchall()
    
    print("🍕 TELEGRAM UPDATES - ЧИТАЕМЫЙ ВИД 🍕")
    print("=" * 60)
    
    for idx, (db_id, update_id, update_data, timestamp) in enumerate(updates, 1):
        print(f"\n📨 СООБЩЕНИЕ #{idx}")
        print(f"🆔 Update ID: {update_id}")
        print(f"🕒 Время: {timestamp}")
        
        try:
            data = json.loads(update_data)
            
            if 'message' in data:
                msg = data['message']
                user = msg['from']
                chat = msg['chat']
                
                print(f"👤 От: {user['first_name']} {user.get('last_name', '')} (@{user.get('username', 'нет')})")
                print(f"🪪 User ID: {user['id']}")
                
                # Конвертируем timestamp в читаемое время
                msg_time = datetime.fromtimestamp(msg['date'])
                print(f"📅 Дата сообщения: {msg_time.strftime('%Y-%m-%d %H:%M:%S')}")
                
                if 'text' in msg:
                    print(f"💬 Текст: {msg['text']}")
                elif 'photo' in msg:
                    photos = msg['photo']
                    print(f"🖼️ Фото: {len(photos)} версий")
                    
                    # Находим фото с максимальным размером
                    largest = max(photos, key=lambda x: x['file_size'])
                    print(f"   📏 Самое большое: {largest['width']}x{largest['height']} ({largest['file_size']} bytes)")
                    print(f"   🆔 File ID: {largest['file_id']}")
                
                print(f"💬 Message ID: {msg['message_id']}")
                
            print("-" * 50)
            
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка парсинга JSON: {e}")
    
    conn.close()

def get_user_stats():
    """Статистика по пользователю"""
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT update_data FROM telegram_updates')
    all_updates = cursor.fetchall()
    
    user_messages = {}
    
    for (update_data,) in all_updates:
        try:
            data = json.loads(update_data)
            if 'message' in data:
                user = data['message']['from']
                user_id = user['id']
                user_name = f"{user['first_name']} {user.get('last_name', '')}"
                
                if user_id not in user_messages:
                    user_messages[user_id] = {
                        'name': user_name,
                        'username': user.get('username', 'нет'),
                        'text_messages': 0,
                        'photo_messages': 0,
                        'total': 0
                    }
                
                user_messages[user_id]['total'] += 1
                
                if 'text' in data['message']:
                    user_messages[user_id]['text_messages'] += 1
                elif 'photo' in data['message']:
                    user_messages[user_id]['photo_messages'] += 1
                    
        except:
            continue
    
    print("\n📊 СТАТИСТИКА ПО ПОЛЬЗОВАТЕЛЯМ")
    print("=" * 50)
    
    for user_id, stats in user_messages.items():
        print(f"👤 {stats['name']} (@{stats['username']})")
        print(f"   🆔 User ID: {user_id}")
        print(f"   📨 Всего сообщений: {stats['total']}")
        print(f"   💬 Текстовых: {stats['text_messages']}")
        print(f"   🖼️ Фото: {stats['photo_messages']}")
        print()
    
    conn.close()

if __name__ == "__main__":
    pretty_view_updates()
    get_user_stats()