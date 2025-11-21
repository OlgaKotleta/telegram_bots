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
        """
        pass
    
    @abstractmethod
    def handle(self, update: Dict[str, Any], db, state: UserState, order_json: Dict[str, Any]) -> bool:
        """
        Обработать апдейт
        """
        pass
    
    def _send_message(self, chat_id: int, text: str, token: str, reply_markup: str = None) -> bool:
        """Утилита для отправки сообщений с клавиатурой"""
        import json
        from urllib.request import urlopen, Request
        from urllib.parse import urlencode
        
        try:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            
            data = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            
            if reply_markup:
                data['reply_markup'] = reply_markup
            
            data = urlencode(data).encode('utf-8')
            
            request = Request(url, data=data, headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            
            with urlopen(request) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            return result.get('ok', False)
            
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False
    
    def _answer_callback_query(self, callback_query_id: str, token: str, text: str = None) -> bool:
        """Ответ на callback query"""
        import json
        from urllib.request import urlopen, Request
        from urllib.parse import urlencode
        
        try:
            url = f"https://api.telegram.org/bot{token}/answerCallbackQuery"
            
            data = {
                'callback_query_id': callback_query_id
            }
            
            if text:
                data['text'] = text
                data['show_alert'] = False
            
            data = urlencode(data).encode('utf-8')
            
            request = Request(url, data=data, headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            
            with urlopen(request) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            return result.get('ok', False)
            
        except Exception as e:
            self.logger.error(f"Error answering callback: {e}")
            return False
    
    def _edit_message_text(self, chat_id: int, message_id: int, text: str, token: str, reply_markup: str = None) -> bool:
        """Редактирование сообщения"""
        import json
        from urllib.request import urlopen, Request
        from urllib.parse import urlencode
        
        try:
            url = f"https://api.telegram.org/bot{token}/editMessageText"
            
            data = {
                'chat_id': chat_id,
                'message_id': message_id,
                'text': text,
                'parse_mode': 'HTML'
            }
            
            if reply_markup:
                data['reply_markup'] = reply_markup
            
            data = urlencode(data).encode('utf-8')
            
            request = Request(url, data=data, headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            
            with urlopen(request) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            return result.get('ok', False)
            
        except Exception as e:
            self.logger.error(f"Error editing message: {e}")
            return False