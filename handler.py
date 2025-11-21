from abc import ABC, abstractmethod
from typing import Dict, Any
from states import UserState
import logging

class Handler(ABC):
    """Абстрактный базовый класс для всех обработчиков"""
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def can_handle(self, update: Dict[str, Any], state: UserState) -> bool:
        """
        Проверить, может ли обработчик обработать данный апдейт
        
        Args:
            update: Данные от Telegram
            state: Текущее состояние пользователя
        """
        pass
    
    @abstractmethod
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        """
        Обработать апдейт
        
        Args:
            update: Данные от Telegram
            db: База данных
            state: Текущее состояние пользователя
            order_json: Текущий заказ пользователя
            
        Returns:
            bool: True - продолжить обработку, False - остановить
        """
        pass
    
    def _send_message(self, chat_id: int, text: str, token: str) -> bool:
        """Утилита для отправки сообщений"""
        import json
        from urllib.request import urlopen, Request
        from urllib.parse import urlencode
        
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            
            data = urlencode({
                'chat_id': chat_id,
                'text': text
            }).encode('utf-8')
            
            request = Request(url, data=data, headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            
            with urlopen(request) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            return result.get('ok', False)
            
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False