import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

class DrinkHandler(Handler):
    """Обработчик выбора напитка"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (state == UserState.WAIT_FOR_DRINKS and
                update.get('message') and 
                update['message'].get('text') and
                update['message']['text'] in ['Кола', 'Фанта', 'Спрайт', 'Без напитка'])
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            drink_choice = message['text']
            
            # Сохраняем выбор напитка (или отсутствие)
            drink = None if drink_choice == 'Без напитка' else drink_choice
            db.update_user_order(user_id, {'drink': drink})
            db.update_user_state(user_id, UserState.WAIT_FOR_ORDER_APPROVE)
            
            # Получаем полный заказ для отображения
            current_order = db.get_user_order(user_id)
            
            response_text = self._format_order_summary(current_order)
            response_text += "\n\nПодтверждаете заказ? (Да/Нет)"
            
            token = self._get_token()
            self._send_message(chat_id, response_text, token)
            logging.info(f"Drink {drink} selected by user {user_id}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in DrinkHandler: {e}")
            return True
    
    def _format_order_summary(self, order: Dict[str, Any]) -> str:
        """Форматирование сводки заказа"""
        summary = "📋 Ваш заказ:\n"
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