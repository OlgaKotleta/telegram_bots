from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class Handler(ABC):
    """Абстрактный базовый класс для всех обработчиков"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def handle(self, update: Dict[str, Any], db) -> bool:
        """
        Обработать апдейт
        
        Args:
            update: Данные от Telegram
            db: Объект базы данных
            
        Returns:
            bool: True - продолжить обработку, False - остановить
        """
        pass
    
    def can_handle(self, update: Dict[str, Any]) -> bool:
        """
        Проверить, может ли обработчик обработать данный апдейт
        """
        return True