import logging
from typing import Dict, Any
from handler import Handler
from states import UserState

class OrderReviewHandler(Handler):
    """Обработчик подтверждения заказа"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (state == UserState.WAIT_FOR_ORDER_APPROVE and
                update.get('message') and 
                update['message'].get('text') in ['Да', 'Нет'])
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            message = update['message']
            chat_id = message['chat']['id']
            user_id = message['from']['id']
            confirmation = message['text']
            
            token = self._get_token()
            
            if confirmation == 'Да':
                # Подтверждаем заказ
                db.update_user_state(user_id, UserState.ORDER_FINISHED)
                
                current_order = db.get_user_order(user_id)
                order_summary = self._format_order_summary(current_order)
                
                response_text = (
                    "✅ Заказ подтвержден!\n\n"
                    f"{order_summary}\n\n"
                    "Спасибо за заказ! Ожидайте доставку 🚗\n\n"
                    "Для нового заказа отправьте /start"
                )
                
                self._send_message(chat_id, response_text, token)
                logging.info(f"Order confirmed by user {user_id}")
                
            else:
                # Отмена заказа
                response_text = (
                    "❌ Заказ отменен.\n\n"
                    "Если хотите начать заново, отправьте /start"
                )
                self._send_message(chat_id, response_text, token)
                db.clear_user_order(user_id)
                logging.info(f"Order cancelled by user {user_id}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in OrderReviewHandler: {e}")
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