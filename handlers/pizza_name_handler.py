import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

class PizzaNameHandler(Handler):
    """Обработчик выбора названия пиццы"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (state == UserState.WAIT_FOR_PIZZA_NAME and
                update.get('message') and 
                update['message'].get('text') and
                update['message']['text'] in ['Маргарита', 'Пепперони', 'Гавайская', 'Четыре сыра'])
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            pizza_name = message['text']
            
            # Сохраняем выбор пиццы
            db.update_user_order(user_id, {'pizza_name': pizza_name})
            db.update_user_state(user_id, UserState.WAIT_FOR_PIZZA_SIZE)
            
            response_text = (
                f"🍕 Отлично! Вы выбрали: {pizza_name}\n\n"
                "Теперь выберите размер:\n"
                "• Маленькая (25см)\n" 
                "• Средняя (30см)\n"
                "• Большая (35см)"
            )
            
            token = self._get_token()
            self._send_message(chat_id, response_text, token)
            logging.info(f"Pizza {pizza_name} selected by user {user_id}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in PizzaNameHandler: {e}")
            return True
    
    def _get_token(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('BOT_TOKEN')