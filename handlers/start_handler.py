import logging
from typing import Dict, Any
from handler import Handler
from states import UserState
from keyboards import InlineKeyboard

class StartHandler(Handler):
    """Обработчик команды /start"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (update.get('message') and 
                update['message'].get('text') == '/start')
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            
            # Сбрасываем состояние и заказ
            db.clear_user_order(user_id)
            db.update_user_state(user_id, UserState.WAIT_FOR_PIZZA_NAME)
            
            welcome_text = (
                "🍕 <b>Добро пожаловать в Pizza Shop!</b>\n\n"
                "Давайте соберем ваш заказ. Выберите пиццу:"
            )
            
            keyboard = InlineKeyboard.create_pizza_keyboard()
            token = self._get_token()
            self._send_message(chat_id, welcome_text, token, keyboard)
            logging.info(f"Start command processed for user {user_id}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in StartHandler: {e}")
            return True
    
    def _get_token(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('BOT_TOKEN')