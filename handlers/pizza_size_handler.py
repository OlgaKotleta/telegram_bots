import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

class PizzaSizeHandler(Handler):
    """Обработчик выбора размера пиццы"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (state == UserState.WAIT_FOR_PIZZA_SIZE and
                update.get('message') and 
                update['message'].get('text') and
                update['message']['text'] in ['Маленькая', 'Средняя', 'Большая'])
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            pizza_size = message['text']
            
            # Сохраняем выбор размера
            db.update_user_order(user_id, {'pizza_size': pizza_size})
            db.update_user_state(user_id, UserState.WAIT_FOR_DRINKS)
            
            response_text = (
                f"📏 Размер: {pizza_size}\n\n"
                "Хотите добавить напиток?\n"
                "• Кола\n"
                "• Фанта\n" 
                "• Спрайт\n"
                "• Без напитка"
            )
            
            token = self._get_token()
            self._send_message(chat_id, response_text, token)
            logging.info(f"Pizza size {pizza_size} selected by user {user_id}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in PizzaSizeHandler: {e}")
            return True
    
    def _get_token(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('BOT_TOKEN')