import sqlite3
import json
import logging
from typing import Optional, Dict, Any
from states import UserState

class Database:
    def __init__(self, db_path: str = 'bot.db'):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self.init_db()
    
    def init_db(self) -> None:
        """Инициализация таблиц в базе данных"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Таблица для хранения всех апдейтов
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS telegram_updates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        update_id INTEGER NOT NULL UNIQUE,
                        update_data TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Таблица пользователей для Pizza Shop
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        state TEXT DEFAULT 'START',
                        order_json TEXT DEFAULT '{}',
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    def save_update(self, update_id: int, update_data: dict) -> bool:
        """Сохранение апдейта в базу данных"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO telegram_updates (update_id, update_data)
                    VALUES (?, ?)
                ''', (update_id, json.dumps(update_data, ensure_ascii=False, indent=2)))
                conn.commit()
                
                self.logger.debug(f"Update saved: {update_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving update: {e}")
            return False
    
    def get_or_create_user(self, user_id: int, username: str = None, 
                          first_name: str = None, last_name: str = None):
        """Получить или создать пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Пытаемся найти пользователя
                cursor.execute(
                    'SELECT user_id, state, order_json FROM users WHERE user_id = ?',
                    (user_id,)
                )
                user = cursor.fetchone()
                
                if user:
                    return user
                
                # Создаем нового пользователя
                cursor.execute('''
                    INSERT INTO users (user_id, username, first_name, last_name)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, username, first_name, last_name))
                
                conn.commit()
                
                # Возвращаем нового пользователя
                return (user_id, 'START', '{}')
                
        except Exception as e:
            self.logger.error(f"Error getting/creating user: {e}")
            return None
    
    def update_user_state(self, user_id: int, state: UserState):
        """Обновить состояние пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET state = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE user_id = ?
                ''', (state.value, user_id))
                conn.commit()
                self.logger.debug(f"User {user_id} state updated to {state.value}")
                return True
        except Exception as e:
            self.logger.error(f"Error updating user state: {e}")
            return False
    
    def update_user_order(self, user_id: int, order_data: Dict[str, Any]):
        """Обновить заказ пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Получаем текущий заказ
                cursor.execute(
                    'SELECT order_json FROM users WHERE user_id = ?',
                    (user_id,)
                )
                result = cursor.fetchone()
                current_order = json.loads(result[0]) if result and result[0] else {}
                
                # Обновляем заказ
                current_order.update(order_data)
                
                # Сохраняем обратно
                cursor.execute('''
                    UPDATE users 
                    SET order_json = ?, updated_at = CURRENT_TIMESTAMP 
                    WHERE user_id = ?
                ''', (json.dumps(current_order, ensure_ascii=False), user_id))
                
                conn.commit()
                self.logger.debug(f"User {user_id} order updated: {order_data}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error updating user order: {e}")
            return False
    
    def get_user_order(self, user_id: int) -> Dict[str, Any]:
        """Получить заказ пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT order_json FROM users WHERE user_id = ?',
                    (user_id,)
                )
                result = cursor.fetchone()
                return json.loads(result[0]) if result and result[0] else {}
        except Exception as e:
            self.logger.error(f"Error getting user order: {e}")
            return {}
    
    def clear_user_order(self, user_id: int):
        """Очистить заказ пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users 
                    SET order_json = '{}', state = 'START', updated_at = CURRENT_TIMESTAMP 
                    WHERE user_id = ?
                ''', (user_id,))
                conn.commit()
                self.logger.debug(f"User {user_id} order cleared")
                return True
        except Exception as e:
            self.logger.error(f"Error clearing user order: {e}")
            return False