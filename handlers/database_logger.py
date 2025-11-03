import logging
import os
import sys
from typing import Dict, Any

# Добавляем корневую папку в путь для импортов
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handler import Handler

class DatabaseLogger(Handler):
    """Обработчик для логирования всех апдейтов в БД"""
    
    def can_handle(self, update: Dict[str, Any]) -> bool:
        """Может обрабатывать все апдейты"""
        return True
    
    def handle(self, update: Dict[str, Any], db) -> bool:
        """Сохраняет апдейт в БД и разрешает продолжение обработки"""
        try:
            update_id = update.get('update_id')
            if update_id:
                db.save_update(update_id, update)
                self.logger.info(f"Update {update_id} saved to database")
            
            # Всегда разрешаем продолжение обработки (требование Д/З)
            return True
            
        except Exception as e:
            self.logger.error(f"Error in DatabaseLogger: {e}")
            # Разрешаем продолжение даже при ошибке
            return True