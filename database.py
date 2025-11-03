import sqlite3
import json
import logging
from typing import Optional

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
                ''', (update_id, json.dumps(update_data, ensure_ascii=False, indent=2)))  # ← ОБА ИСПРАВЛЕНИЯ ЗДЕСЬ
                conn.commit()
                
                self.logger.debug(f"Update saved: {update_id}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving update: {e}")
            return False
    
    def get_updates_count(self) -> int:
        """Получение количества сохраненных апдейтов"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT COUNT(*) FROM telegram_updates')
                return cursor.fetchone()[0]
        except Exception as e:
            self.logger.error(f"Error getting updates count: {e}")
            return 0