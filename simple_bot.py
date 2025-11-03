import sqlite3
import json
import requests
import time
import logging
import os
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SimpleBot:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv('BOT_TOKEN')
        self.db_path = 'bot.db'
        self.setup_database()
    
    def setup_database(self):
        """Настройка базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS telegram_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                update_id INTEGER NOT NULL UNIQUE,
                update_data TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("Database setup complete")
    
    def get_last_offset(self):
        """Получить последний offset из базы"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(update_id) FROM telegram_updates")
        result = cursor.fetchone()
        conn.close()
        return result[0] + 1 if result[0] else 0
    
    def save_update(self, update_id, update_data):
        """Сохранить апдейт в базу"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT OR IGNORE INTO telegram_updates (update_id, update_data) VALUES (?, ?)",
                (update_id, json.dumps(update_data))
            )
            conn.commit()
            logging.info(f"✅ Saved update {update_id} to database")
            return True
        except Exception as e:
            logging.error(f"❌ Error saving update {update_id}: {e}")
            return False
        finally:
            conn.close()
    
    def process_message(self, message):
        """Обработать сообщение"""
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        if text:
            # Эхо-ответ
            response_text = f"Эхо: {text}"
            self.send_message(chat_id, response_text)
            logging.info(f"Sent echo: {response_text}")
    
    def send_message(self, chat_id, text):
        """Отправить сообщение"""
        try:
            response = requests.post(
                f"https://api.telegram.org/bot{self.token}/sendMessage",
                data={'chat_id': chat_id, 'text': text},
                timeout=10
            )
            return response.json().get('ok', False)
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            return False
    
    def run(self):
        """Запуск бота"""
        offset = self.get_last_offset()
        logging.info(f"Starting bot with offset: {offset}")
        
        while True:
            try:
                # Получаем обновления
                response = requests.post(
                    f"https://api.telegram.org/bot{self.token}/getUpdates",
                    data={'offset': offset, 'timeout': 30},
                    timeout=35
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok'):
                        updates = data['result']
                        
                        if updates:
                            logging.info(f"Received {len(updates)} new updates")
                            
                        for update in updates:
                            update_id = update['update_id']
                            
                            # Сохраняем в базу
                            self.save_update(update_id, update)
                            
                            # Обрабатываем сообщение
                            if 'message' in update:
                                self.process_message(update['message'])
                            
                            # Обновляем offset
                            offset = update_id + 1
                            logging.info(f"Offset updated to: {offset}")
                    
                else:
                    logging.error(f"HTTP error: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                # Таймаут - это нормально для long polling
                continue
            except KeyboardInterrupt:
                logging.info("Bot stopped by user")
                break
            except Exception as e:
                logging.error(f"Unexpected error: {e}")
                time.sleep(5)  # Пауза перед повторной попыткой

if __name__ == "__main__":
    bot = SimpleBot()
    bot.run()