import logging
from typing import List
from handler import Handler

class Dispatcher:
    def __init__(self):
        self.handlers: List[Handler] = []
        self.logger = logging.getLogger(__name__)
        self.logger.info("Dispatcher initialized")
    
    def register_handler(self, handler: Handler):
        """Регистрация обработчика"""
        self.handlers.append(handler)
        self.logger.info(f"Handler registered: {handler.__class__.__name__}")
    
    def process_update(self, update: dict, db) -> None:
        """Обработка обновления через цепочку обработчиков"""
        self.logger.debug(f"Processing update: {update.get('update_id')}")
        
        for handler in self.handlers:
            if handler.can_handle(update):
                try:
                    continue_processing = handler.handle(update, db)
                    self.logger.debug(f"Handler {handler.__class__.__name__} processed update")
                    
                    if not continue_processing:
                        break
                        
                except Exception as e:
                    self.logger.error(f"Error in handler {handler.__class__.__name__}: {e}")
                    continue