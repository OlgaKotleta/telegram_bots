import logging
from typing import Dict, Any
from handler import Handler
from states import UserState
from keyboards import InlineKeyboard

class PizzaSizeHandler(Handler):
    """Обработчик выбора размера пиццы (через callback)"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (state == UserState.WAIT_FOR_PIZZA_SIZE and
                update.get('callback_query') and
                update['callback_query']['data'].startswith('size_'))
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            callback_query = update['callback_query']
            callback_data = callback_query['data']
            message = callback_query['message']
            chat_id = message['chat']['id']
            message_id = message['message_id']
            user_id = callback_query['from']['id']
            callback_id = callback_query['id']
            
            # Маппинг callback_data на размеры
            size_map = {
                'size_small': 'Маленькая',
                'size_medium': 'Средняя',
                'size_large': 'Большая'
            }
            
            pizza_size = size_map.get(callback_data)
            
            if pizza_size:
                # Сохраняем выбор размера
                db.update_user_order(user_id, {'pizza_size': pizza_size})
                db.update_user_state(user_id, UserState.WAIT_FOR_DRINKS)
                
                # Отвечаем на callback
                token = self._get_token()
                self._answer_callback_query(callback_id, token, f"Размер: {pizza_size}")
                
                # Обновляем сообщение
                response_text = (
                    f"📏 <b>Размер: {pizza_size}</b>\n\n"
                    "Хотите добавить напиток?"
                )
                
                keyboard = InlineKeyboard.create_drink_keyboard()
                self._edit_message_text(chat_id, message_id, response_text, token, keyboard)
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