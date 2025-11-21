import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

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
                "🍕 Добро пожаловать в Pizza Shop!\n\n"
                "Давайте соберем ваш заказ. Выберите пиццу:\n"
                "• Маргарита\n"
                "• Пепперони\n" 
                "• Гавайская\n"
                "• Четыре сыра"
            )
            
            token = self._get_token()
            self._send_message(chat_id, welcome_text, token)
            logging.info(f"Start command processed for user {user_id}")
            
            return False  # Останавливаем обработку
            
        except Exception as e:
            self.logger.error(f"Error in StartHandler: {e}")
            return True
    
    def _get_token(self):
        """Получить токен из переменных окружения"""
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('BOT_TOKEN')