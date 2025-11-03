import logging
import json
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from dispatcher import Dispatcher

logger = logging.getLogger(__name__)

def make_request(token: str, method: str, data: dict = None) -> dict:
    """Выполнение HTTP запроса к Telegram API"""
    url = f"https://api.telegram.org/bot{token}/{method}"
    
    if data:
        data = urlencode(data).encode('utf-8')
    
    request = Request(url, data=data, headers={
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    
    try:
        with urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
        return result
    except Exception as e:
        logger.error(f"Request error: {e}")
        return {'ok': False, 'error': str(e)}

def start_long_polling(dispatcher: Dispatcher, db, token: str):
    """Запуск long polling цикла"""
    offset = 0
    logger.info("Starting long polling...")
    
    while True:
        try:
            # Получаем обновления
            data = {'offset': offset, 'timeout': 30}
            result = make_request(token, 'getUpdates', data)
            
            if result.get('ok'):
                updates = result['result']
                
                for update in updates:
                    offset = update['update_id'] + 1
                    
                    # Передаем обновление в диспетчер
                    dispatcher.process_update(update, db)
                    
            else:
                logger.error(f"Error getting updates: {result}")
                
        except KeyboardInterrupt:
            logger.info("Long polling stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in long polling: {e}")
            continue