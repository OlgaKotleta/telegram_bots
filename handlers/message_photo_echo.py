import logging
import json
import os
from typing import Dict, Any
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from handler import Handler

class MessagePhotoEcho(Handler):
    """Обработчик для эхо-ответов на фото"""
    
    def can_handle(self, update: Dict[str, Any]) -> bool:
        """Может обрабатывать только сообщения с фото"""
        return ('message' in update and 
                'photo' in update['message'])
    
    def handle(self, update: Dict[str, Any], db) -> bool:
        """Отправляет эхо-фото"""
        try:
            message = update['message']
            chat_id = message['chat']['id']
            photos = message['photo']
            
            # Выбираем фото с максимальным размером
            largest_photo = max(photos, key=lambda x: x['file_size'])
            file_id = largest_photo['file_id']
            
            # Отправляем то же фото обратно
            self._send_photo(chat_id, file_id)
            self.logger.info(f"Photo echo sent, file_id: {file_id}")
            
            return True  # Продолжаем обработку
            
        except Exception as e:
            self.logger.error(f"Error in MessagePhotoEcho: {e}")
            return True
    
    def _send_photo(self, chat_id: int, file_id: str) -> None:
        """Утилита для отправки фото"""
        try:
            token = os.getenv('BOT_TOKEN')
            url = f"https://api.telegram.org/bot{token}/sendPhoto"
            
            data = urlencode({
                'chat_id': chat_id,
                'photo': file_id,
                'caption': 'Эхо-фото 📸'
            }).encode('utf-8')
            
            request = Request(url, data=data, headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            })
            
            with urlopen(request) as response:
                result = json.loads(response.read().decode('utf-8'))
                
            if not result.get('ok'):
                self.logger.error(f"Failed to send photo: {result}")
                
        except Exception as e:
            self.logger.error(f"Error sending photo: {e}")