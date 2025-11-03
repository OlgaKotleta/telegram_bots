import logging
import json
import os
from typing import Dict, Any
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from handler import Handler

class MessageTextEcho(Handler):
    
    def can_handle(self, update: Dict[str, Any]) -> bool:
        return ('message' in update and 
                'text' in update['message'])
    
    def handle(self, update: Dict[str, Any], db) -> bool:
        try:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '').strip()
            
            if not text:
                return True
            
            # Обработка команд
            if text == '/start':
                welcome_text = (
                    "👋 Привет! Я эхо-бот\n\n"
                    "Я умею:\n"
                    "• Отвечать эхом на текстовые сообщения\n"
                    "• Отправлять обратно фото\n"
                    "• Сохранять все сообщения в базу данных\n\n"
                    "Просто напиши мне что-нибудь или отправь фото!"
                )
                self._send_message(chat_id, welcome_text)
                return False
                
            elif text == '/help':
                help_text = (
                    "📖 Справка по боту:\n\n"
                    "Доступные команды:\n"
                    "/start - начать работу с ботом\n"
                    "/help - показать эту справку\n\n"
                    "Функциональность:\n"
                    "• 💬 Текстовые сообщения - получаешь эхо-ответ\n"
                    "• 🖼️ Фото - получаешь то же фото обратно\n"
                    "• 📊 Все сообщения сохраняются в базу данных"
                )
                self._send_message(chat_id, help_text)
                return False
            
            # Эхо-ответ для обычных сообщений
            else:
                response_text = f"Эхо: {text}"
                self._send_message(chat_id, response_text)
                self.logger.info(f"Echo response sent: {response_text}")
                return True  
            
        except Exception as e:
            self.logger.error(f"Error in MessageTextEcho: {e}")
            return True
    
    def _send_message(self, chat_id: int, text: str) -> None:
        try:
            token = os.getenv('BOT_TOKEN')
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            
            data = urlencode({
                'chat_id': chat_id,
                'text': text
            }).encode('utf-8')
            
            request = Request(url, data=data, headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            
            with urlopen(request) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            if not result.get('ok'):
                self.logger.error(f"Failed to send message: {result}")
                
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")