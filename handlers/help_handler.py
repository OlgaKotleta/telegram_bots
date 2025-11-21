import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

class HelpHandler(Handler):
    """Обработчик команды /help"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (update.get('message') and 
                update['message'].get('text') == '/help')
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        """Отправляет справку по боту"""
        try:
            message = update['message']
            chat_id = message['chat']['id']
            
            help_text = (
                "🍕 Pizza Shop Bot - Справка\n\n"
                "📋 Доступные команды:\n"
                "/start - Начать заказ пиццы\n"
                "/help - Показать эту справку\n\n"
                "🔧 Процесс заказа:\n"
                "1. /start - начать заказ\n"
                "2. Выбрать пиццу (Маргарита, Пепперони, etc.)\n"
                "3. Выбрать размер (Маленькая, Средняя, Большая)\n"
                "4. Выбрать напиток (Кола, Фанта, etc.)\n"
                "5. Подтвердить заказ\n\n"
                "💾 Все заказы сохраняются в базу данных"
            )
            
            token = self._get_token()
            self._send_message(chat_id, help_text, token)
            logging.info(f"Help command processed")
            
            return False  # Останавливаем обработку
            
        except Exception as e:
            self.logger.error(f"Error in HelpHandler: {e}")
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