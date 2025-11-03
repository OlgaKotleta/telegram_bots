import logging
import json
from typing import Dict, Any
from handler import Handler

class DatabaseLogger(Handler):
    """Обработчик для логирования всех апдейтов в БД"""
    
    def can_handle(self, update: Dict[str, Any]) -> bool:
        return True
    
    def handle(self, update: Dict[str, Any], db) -> bool:
        """Сохраняет апдейт в БД и разрешает продолжение обработки"""
        try:
            update_id = update.get('update_id')
            if update_id:
                db.save_update(update_id, update)
                self.logger.info(f"Update {update_id} saved to database")
            
            # Всегда разрешаем продолжение обработки
            return True
            
        except Exception as e:
            self.logger.error(f"Error in DatabaseLogger: {e}")
            return True