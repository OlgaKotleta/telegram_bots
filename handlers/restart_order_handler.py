import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

class RestartOrderHandler(Handler):
    """Обработчик начала заказа сначала"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (update.get('message') and 
                update['message'].get('text') == '/start')
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            
            # Сбрасываем заказ
            db.clear_user_order(user_id)
            db.update_user_state(user_id, UserState.WAIT_FOR_PIZZA_NAME)
            
            response_text = (
                "🔄 Начинаем новый заказ!\n\n"
                "Выберите пиццу:\n"
                "• Маргарита\n"
                "• Пепперони\n"
                "• Гавайская\n"
                "• Четыре сыра"
            )
            
            token = self._get_token()
            self._send_message(chat_id, response_text, token)
            logging.info(f"Order restarted by user {user_id}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in RestartOrderHandler: {e}")
            return True
    
    def _get_token(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('BOT_TOKEN')