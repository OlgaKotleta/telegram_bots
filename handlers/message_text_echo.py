import logging
import json
import os
import sys
from typing import Dict, Any
from urllib.request import urlopen, Request
from urllib.parse import urlencode

# Добавляем корневую папку в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import Handler

class MessageTextEcho(Handler):
    """Обработчик для эхо-ответов на текстовые сообщения"""
    
    def can_handle(self, update: Dict[str, Any]) -> bool:
        """Может обрабатывать только текстовые сообщения"""
        return ('message' in update and 
                'text' in update['message'] and
                not update['message']['text'].startswith('/'))
    
    def handle(self, update: Dict[str, Any], db) -> bool:
        """Отправляет эхо-ответ и разрешает продолжение обработки"""
        try:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '').strip()
            
            if not text:
                return True
            
            # Эхо-ответ
            response_text = f"Эхо: {text}"
            self._send_message(chat_id, response_text)
            self.logger.info(f"Echo response sent: {response_text}")
            
            # Разрешаем продолжение обработки
            return True
            
        except Exception as e:
            self.logger.error(f"Error in MessageTextEcho: {e}")
            return True
    
    def _send_message(self, chat_id: int, text: str) -> None:
        """Утилита для отправки сообщений"""
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