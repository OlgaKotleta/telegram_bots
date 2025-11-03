import os
import logging
from dotenv import load_dotenv

from database import Database
from dispatcher import Dispatcher
from long_polling import start_long_polling
from handlers import DatabaseLogger, MessageTextEcho, MessagePhotoEcho

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

def main():
    """Основная функция запуска бота"""
    # Загрузка переменных окружения
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        raise ValueError("BOT_TOKEN not found in environment variables")
    
    # Инициализация компонентов
    db = Database()
    dispatcher = Dispatcher()
    
    # Регистрация обработчиков (важен порядок!)
    dispatcher.register_handler(DatabaseLogger())      # Первый - логирует всё
    dispatcher.register_handler(MessageTextEcho())    # Текстовые сообщения
    dispatcher.register_handler(MessagePhotoEcho())   # Фото
    
    logging.info("Bot started with dispatcher pattern")
    logging.info("Registered handlers: DatabaseLogger, MessageTextEcho, MessagePhotoEcho")
    
    # Запуск long polling
    try:
        start_long_polling(dispatcher, db, token)
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.critical(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()