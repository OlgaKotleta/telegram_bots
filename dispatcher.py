import logging
from typing import List
from handler import Handler
from database import Database
from states import UserState

class Dispatcher:
    def __init__(self, db: Database):
        self.handlers: List[Handler] = []
        self.db = db
        self.logger = logging.getLogger(__name__)
        self.logger.info("Dispatcher initialized")
    
    def register_handler(self, handler: Handler):
        """Регистрация обработчика"""
        self.handlers.append(handler)
        self.logger.info(f"Handler registered: {handler.__class__.__name__}")
    
    def process_update(self, update: dict, token: str) -> None:
        """Обработка обновления через цепочку обработчиков"""
        self.logger.debug(f"Processing update: {update.get('update_id')}")
        
        # Получаем информацию о пользователе
        user_info = self._extract_user_info(update)
        if not user_info:
            return
        
        user_id, state_str, order_json_str = user_info
        
        try:
            state = UserState(state_str)
            order_json = eval(order_json_str) if order_json_str and order_json_str != '{}' else {}
        except:
            state = UserState.START
            order_json = {}
        
        for handler in self.handlers:
            if handler.can_handle(update, state):
                try:
                    continue_processing = handler.handle(update, self.db, state, order_json)
                    self.logger.debug(f"Handler {handler.__class__.__name__} processed update")
                    
                    if not continue_processing:
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error in handler {handler.__class__.__name__}: {e}")
                    continue
    
    def _extract_user_info(self, update: dict):
        """Извлечение информации о пользователе из апдейта"""
        try:
            if 'message' in update:
                user = update['message']['from']
            elif 'callback_query' in update:
                user = update['callback_query']['from']
            else:
                return None
            
            user_id = user['id']
            username = user.get('username')
            first_name = user.get('first_name')
            last_name = user.get('last_name')
            
            return self.db.get_or_create_user(user_id, username, first_name, last_name)
            
        except Exception as e:
            self.logger.error(f"Error extracting user info: {e}")
            return None