import logging
from typing import Dict, Any
from handler import Handler
from states import UserState
from keyboards import InlineKeyboard

class OrderReviewHandler(Handler):
    """Обработчик подтверждения заказа (через callback)"""
    
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        return (state == UserState.WAIT_FOR_ORDER_APPROVE and
                update.get('callback_query') and
                update['callback_query']['data'].startswith('confirm_'))
    
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        try:
            callback_query = update['callback_query']
            callback_data = callback_query['data']
            message = callback_query['message']
            chat_id = message['chat']['id']
            message_id = message['message_id']
            user_id = callback_query['from']['id']
            callback_id = callback_query['id']
            
            token = self._get_token()
            
            # Отвечаем на callback сразу
            if callback_data == 'confirm_yes':
                self._answer_callback_query(callback_id, token, "Заказ подтвержден!")
            else:
                self._answer_callback_query(callback_id, token, "Заказ отменен")
            
            if callback_data == 'confirm_yes':
                # Подтверждаем заказ
                db.update_user_state(user_id, UserState.ORDER_FINISHED)
                
                current_order = db.get_user_order(user_id)
                order_summary = self._format_order_summary(current_order)
                
                # Обновляем сообщение
                response_text = (
                    "✅ <b>Заказ подтвержден!</b>\n\n"
                    f"{order_summary}\n\n"
                    "<i>Спасибо за заказ! Ожидайте доставку 🚗</i>\n\n"
                    "Для нового заказа отправьте /start"
                )
                
                # Убираем клавиатуру
                empty_keyboard = '{"inline_keyboard":[]}'
                self._edit_message_text(chat_id, message_id, response_text, token, empty_keyboard)
                logging.info(f"Order confirmed by user {user_id}")
                
            else:
                # Отмена заказа
                response_text = "❌ <b>Заказ отменен.</b>\n\nЕсли хотите начать заново, отправьте /start"
                empty_keyboard = '{"inline_keyboard":[]}'
                self._edit_message_text(chat_id, message_id, response_text, token, empty_keyboard)
                db.clear_user_order(user_id)
                logging.info(f"Order cancelled by user {user_id}")
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in OrderReviewHandler: {e}")
            try:
                token = self._get_token()
                self._answer_callback_query(callback_id, token, "Произошла ошибка")
            except:
                pass
            return True
    
    def _format_order_summary(self, order: Dict[str, Any]) -> str:
        """Форматирование сводки заказа"""
        summary = "📋 <b>Ваш заказ:</b>\n"
        summary += f"🍕 Пицца: {order.get('pizza_name', 'Не выбрано')}\n"
        summary += f"📏 Размер: {order.get('pizza_size', 'Не выбрано')}\n"
        
        drink = order.get('drink')
        if not drink:
            summary += "🥤 Напиток: Без напитка\n"
        else:
            summary += f"🥤 Напиток: {drink}\n"
            
        return summary
    
    def _get_token(self):
        import os
        from dotenv import load_dotenv
        load_dotenv()
        return os.getenv('BOT_TOKEN')