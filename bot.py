import os
import json
import logging
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from dotenv import load_dotenv
from database import Database

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class TelegramBot:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv('BOT_TOKEN')
        if not self.token:
            raise ValueError("BOT_TOKEN not found in environment variables")
        
        self.base_url = f"https://api.telegram.org/bot{self.token}"
        self.db = Database()
        self.offset = 0
        logging.info("Bot initialized")
    
    def make_request(self, method, data=None):
        """Выполнение HTTP запроса к Telegram API"""
        url = f"{self.base_url}/{method}"
        
        if data:
            data = urlencode(data).encode('utf-8')
        
        request = Request(url, data=data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        
        with urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
        
        return result
    
    def get_updates(self):
        """Получение обновлений от Telegram"""
        data = {'offset': self.offset, 'timeout': 30}
        try:
            result = self.make_request('getUpdates', data)
            if result['ok']:
                return result['result']
            return []
        except Exception as e:
            logging.error(f"Error getting updates: {e}")
            return []
    
    def send_message(self, chat_id, text):
        """Отправка сообщения"""
        data = {'chat_id': chat_id, 'text': text}
        return self.make_request('sendMessage', data)
    
    def process_message(self, message):
        """Обработка входящего сообщения"""
        chat_id = message['chat']['id']
        user_id = message['from']['id']
        text = message.get('text', '')
        
        # Сохраняем сообщение в БД
        self.db.save_message(chat_id, user_id, text)
        
        # Эхо-ответ
        if text:
            response_text = f"Эхо: {text}"
            self.send_message(chat_id, response_text)
            logging.info(f"Echo response sent: {response_text}")
    
    def run(self):
        """Основной цикл бота"""
        logging.info("Bot started polling...")
        
        while True:
            updates = self.get_updates()
            
            for update in updates:
                self.offset = update['update_id'] + 1
                
                if 'message' in update:
                    self.process_message(update['message'])

if __name__ == "__main__":
    bot = TelegramBot()
    bot.run()