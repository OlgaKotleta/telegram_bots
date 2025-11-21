import logging
from typing import Dict, Any
from handler import Handler
from states import UserState
from keyboards import InlineKeyboard

class DrinkHandler(Handler):
    """Обработчик выбора напитка (через callback)"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (state == UserState.WAIT_FOR_DRINKS and
                update.get('callback_query') and
                update['callback_query']['data'].startswith('drink_'))
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            callback_query = update['callback_query']
            callback_data = callback_query['data']
            message = callback_query['message']
            chat_id = message['chat']['id']
            message_id = message['message_id']
            user_id = callback_query['from']['id']
            callback_id = callback_query['id']
            
            # Маппинг callback_data на напитки
            drink_map = {
                'drink_cola': 'Кола',
                'drink_fanta': 'Фанта',
                'drink_sprite': 'Спрайт',
                'drink_none': None
            }
            
            drink = drink_map.get(callback_data)
            
            if drink is not None:  # включая None для "Без напитка"
                # Сохраняем выбор напитка
                db.update_user_order(user_id, {'drink': drink})
                db.update_user_state(user_id, UserState.WAIT_FOR_ORDER_APPROVE)
                
                # Отвечаем на callback
                token = self._get_token()
                drink_text = "Без напитка" if drink is None else drink
                self._answer_callback_query(callback_id, token, f"Напиток: {drink_text}")
                
                # Получаем полный заказ для отображения
                current_order = db.get_user_order(user_id)
                response_text = self._format_order_summary(current_order)
                response_text += "\n\n<b>Подтверждаете заказ?</b>"
                
                keyboard = InlineKeyboard.create_confirmation_keyboard()
                self._edit_message_text(chat_id, message_id, response_text, token, keyboard)
                logging.info(f"Drink {drink} selected by user {user_id}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in DrinkHandler: {e}")
            return True
    
    def _format_order_summary(self, order: Dict[str, Any]) -> str:
        """Форматирование сводки заказа"""
        summary = "📋 <b>Ваш заказ:</b>\n"
        summary += f"🍕 Пицца: {order.get('pizza_name', 'Не выбрано')}\n"
        summary += f"📏 Размер: {order.get('pizza_size', 'Не выбрано')}\n"
        
        drink = order.get('drink')
        if drink:
            summary += f"🥤 Напиток: {drink}\n"
        else:
            summary += "🥤 Напиток: Без напитка\n"
            
        return summary
    
    def _get_token(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('BOT_TOKEN')