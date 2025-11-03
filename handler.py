from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

class Handler(ABC):
    """Абстрактный базовый класс для всех обработчиков"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def can_handle(self, update: Dict[str, Any]) -> bool:
        """
        Проверить, может ли обработчик обработать данный апдейт
        """
        pass
    
    @abstractmethod
    def handle(self, update: Dict[str, Any], db) -> bool:
        """
        Обработать апдейт
        
        Returns:
            bool: True - продолжить обработку, False - остановить
        """
        pass