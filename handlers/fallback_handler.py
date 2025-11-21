import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

class FallbackHandler(Handler):
    """Обработчик для сообщений, которые не попали в другие обработчики"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        """Обрабатывает любые текстовые сообщения в состоянии START"""
        return (state == UserState.START and
                update.get('message') and 
                'text' in update['message'] and
                not update['message']['text'].startswith('/'))
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        """Отправляет инструкцию по началу заказа"""
        try:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            
            help_text = (
                "🤖 Я бот Pizza Shop!\n\n"
                "Чтобы начать заказ пиццы, отправьте команду:\n"
                "🍕 /start\n\n"
                "Или используйте:\n"
                "📖 /help - для справки"
            )
            
            token = self._get_token()
            self._send_message(chat_id, help_text, token)
            logging.info(f"Fallback handler sent help to user {user_id}")
            
            return False  # Останавливаем обработку
            
        except Exception as e:
            self.logger.error(f"Error in FallbackHandler: {e}")
            return True
    
    def _get_token(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('BOT_TOKEN')
    
    def _send_message(self, chat_id: int, text: str, token: str) -> bool:
        import json
        from urllib.request import urlopen, Request
        from urllib.parse import urlencode
        
        try:
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
                
            return result.get('ok', False)
            
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False