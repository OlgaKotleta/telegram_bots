import logging
from typing import Dict, Any
from handler import Handler
from states import UserState
from keyboards import InlineKeyboard

class PizzaNameHandler(Handler):
    """Обработчик выбора названия пиццы (через callback)"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (state == UserState.WAIT_FOR_PIZZA_NAME and
                update.get('callback_query') and
                update['callback_query']['data'].startswith('pizza_'))
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            callback_query = update['callback_query']
            callback_data = callback_query['data']
            message = callback_query['message']
            chat_id = message['chat']['id']
            message_id = message['message_id']
            user_id = callback_query['from']['id']
            callback_id = callback_query['id']
            
            # Маппинг callback_data на названия пицц
            pizza_map = {
                'pizza_margarita': 'Маргарита',
                'pizza_pepperoni': 'Пепперони',
                'pizza_hawaiian': 'Гавайская',
                'pizza_cheese': 'Четыре сыра'
            }
            
            pizza_name = pizza_map.get(callback_data)
            
            if pizza_name:
                # Сохраняем выбор пиццы
                db.update_user_order(user_id, {'pizza_name': pizza_name})
                db.update_user_state(user_id, UserState.WAIT_FOR_PIZZA_SIZE)
                
                # Отвечаем на callback
                token = self._get_token()
                self._answer_callback_query(callback_id, token, f"Выбрана: {pizza_name}")
                
                # Обновляем сообщение
                response_text = (
                    f"🍕 <b>Отлично! Вы выбрали: {pizza_name}</b>\n\n"
                    "Теперь выберите размер:"
                )
                
                keyboard = InlineKeyboard.create_size_keyboard()
                self._edit_message_text(chat_id, message_id, response_text, token, keyboard)
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