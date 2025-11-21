import os
import logging
from dotenv import load_dotenv

from database import Database
from dispatcher import Dispatcher
from long_polling import start_long_polling
from handlers.database_logger import DatabaseLogger
from handlers.start_handler import StartHandler
from handlers.help_handler import HelpHandler
from handlers.pizza_name_handler import PizzaNameHandler
from handlers.pizza_size_handler import PizzaSizeHandler
from handlers.drink_handler import DrinkHandler
from handlers.order_review_handler import OrderReviewHandler
from handlers.restart_order_handler import RestartOrderHandler
from handlers.fallback_handler import FallbackHandler

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
    dispatcher = Dispatcher(db)
    
    # Регистрация обработчиков (ВАЖЕН ПОРЯДОК!)
    dispatcher.register_handler(DatabaseLogger())      # 1. Логирует всё в БД
    dispatcher.register_handler(StartHandler())        # 2. Команда /start
    dispatcher.register_handler(HelpHandler())         # 3. Команда /help  
    dispatcher.register_handler(RestartOrderHandler()) # 4. Перезапуск заказа
    dispatcher.register_handler(PizzaNameHandler())    # 5. Выбор пиццы
    dispatcher.register_handler(PizzaSizeHandler())    # 6. Выбор размера
    dispatcher.register_handler(DrinkHandler())        # 7. Выбор напитка
    dispatcher.register_handler(OrderReviewHandler())  # 8. Подтверждение заказа
    dispatcher.register_handler(FallbackHandler())     # 9. Обработка остальных сообщений
    
    logging.info("Pizza Shop Bot started")
    logging.info("Registered handlers for pizza ordering workflow")
    
    # Запуск long polling
    try:
        start_long_polling(dispatcher, db, token)
    except KeyboardInterrupt:
        logging.info("Bot stopped by user")
    except Exception as e:
        logging.critical(f"Bot crashed: {e}")

if __name__ == "__main__":
    main()