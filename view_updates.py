import sqlite3
import json
from datetime import datetime

def view_telegram_updates():
    """Просмотр telegram_updates в структурированном виде"""
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    
    # Получаем все записи
    cursor.execute('''
        SELECT id, update_id, update_data, timestamp 
        FROM telegram_updates 
        ORDER BY timestamp DESC
    ''')
    
    updates = cursor.fetchall()
    
    print("=" * 80)
    print("TELEGRAM UPDATES - STRUCTURED VIEW")
    print("=" * 80)
    
    for idx, (db_id, update_id, update_data, timestamp) in enumerate(updates, 1):
        print(f"\n--- Update #{idx} | DB ID: {db_id} | Update ID: {update_id} ---")
        print(f"Timestamp: {timestamp}")
        
        try:
            data = json.loads(update_data)
            
            if 'message' in data:
                msg = data['message']
                print(f"Message ID: {msg.get('message_id')}")
                print(f"From: {msg['from'].get('first_name')} {msg['from'].get('last_name')} (@{msg['from'].get('username')})")
                print(f"User ID: {msg['from'].get('id')}")
                
                if 'text' in msg:
                    print(f"Text: {msg['text']}")
                elif 'photo' in msg:
                    photos = msg['photo']
                    print(f"Photo: {len(photos)} versions")
                    for i, photo in enumerate(photos):
                        print(f"  Version {i+1}: {photo['width']}x{photo['height']} ({photo['file_size']} bytes)")
                
                print(f"Date: {datetime.fromtimestamp(msg['date']).strftime('%Y-%m-%d %H:%M:%S')}")
                
            else:
                print("No message in update")
                print(f"Raw keys: {list(data.keys())}")
                
        except json.JSONDecodeError as e:
            print(f"ERROR parsing JSON: {e}")
            print(f"Raw data: {update_data[:100]}...")
        
        print("-" * 60)
    
    conn.close()

def get_update_stats():
    """Статистика по апдейтам"""
    conn = sqlite3.connect('bot.db')
    cursor = conn.cursor()
    
    # Общая статистика
    cursor.execute('SELECT COUNT(*) FROM telegram_updates')
    total = cursor.fetchone()[0]
    
    cursor.execute('''
        SELECT MIN(timestamp), MAX(timestamp) FROM telegram_updates
    ''')
    min_time, max_time = cursor.fetchone()
    
    # Статистика по типам сообщений
    cursor.execute('SELECT update_data FROM telegram_updates')
    all_updates = cursor.fetchall()
    
    text_count = 0
    photo_count = 0
    other_count = 0
    
    for (update_data,) in all_updates:
        try:
            data = json.loads(update_data)
            if 'message' in data:
                msg = data['message']
                if 'text' in msg:
                    text_count += 1
                elif 'photo' in msg:
                    photo_count += 1
                else:
                    other_count += 1
        except:
            other_count += 1
    
    print("\n" + "=" * 50)
    print("UPDATE STATISTICS")
    print("=" * 50)
    print(f"Total updates: {total}")
    print(f"Time range: {min_time} to {max_time}")
    print(f"Text messages: {text_count}")
    print(f"Photo messages: {photo_count}")
    print(f"Other messages: {other_count}")
    
    conn.close()

if __name__ == "__main__":
    view_telegram_updates()
    get_update_stats()