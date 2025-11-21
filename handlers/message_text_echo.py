import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

class MessageTextEcho(Handler):
    """Обработчик для эхо-ответов на текстовые сообщения (резервный)"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        """Может обрабатывать только текстовые сообщения не в процессе заказа"""
        return (state == UserState.START and
                update.get('message') and 
                'text' in update['message'])
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        """Отправляет эхо-ответ"""
        try:
            message = update['message']
            chat_id = message['chat']['id']
            text = message.get('text', '').strip()
            
            if text and not text.startswith('/'):
                response_text = f"Эхо: {text}"
                self._send_message(chat_id, response_text)
                self.logger.info(f"Echo response sent: {response_text}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error in MessageTextEcho: {e}")
            return True
    
    def _send_message(self, chat_id: int, text: str) -> None:
        """Утилита для отправки сообщений"""
        import json
        import os
        from urllib.request import urlopen, Request
        from urllib.parse import urlencode
        
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