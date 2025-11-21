import json
from typing import List, Dict, Any

class InlineKeyboard:
    """Класс для создания inline клавиатур"""
    
    @staticmethod
    def create_pizza_keyboard():
        """Клавиатура для выбора пиццы"""
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🍕 Маргарита", "callback_data": "pizza_margarita"},
                    {"text": "🍕 Пепперони", "callback_data": "pizza_pepperoni"}
                ],
                [
                    {"text": "🍕 Гавайская", "callback_data": "pizza_hawaiian"},
                    {"text": "🍕 Четыре сыра", "callback_data": "pizza_cheese"}
                ]
            ]
        }
        return json.dumps(keyboard)
    
    @staticmethod
    def create_size_keyboard():
        """Клавиатура для выбора размера"""
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "📏 Маленькая (25см)", "callback_data": "size_small"},
                    {"text": "📏 Средняя (30см)", "callback_data": "size_medium"}
                ],
                [
                    {"text": "📏 Большая (35см)", "callback_data": "size_large"}
                ]
            ]
        }
        return json.dumps(keyboard)
    
    @staticmethod
    def create_drink_keyboard():
        """Клавиатура для выбора напитка"""
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🥤 Кола", "callback_data": "drink_cola"},
                    {"text": "🥤 Фанта", "callback_data": "drink_fanta"}
                ],
                [
                    {"text": "🥤 Спрайт", "callback_data": "drink_sprite"},
                    {"text": "🚫 Без напитка", "callback_data": "drink_none"}
                ]
            ]
        }
        return json.dumps(keyboard)
    
    @staticmethod
    def create_confirmation_keyboard():
        """Клавиатура для подтверждения заказа"""
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ Да, подтверждаю", "callback_data": "confirm_yes"},
                    {"text": "❌ Нет, отменить", "callback_data": "confirm_no"}
                ]
            ]
        }
        return json.dumps(keyboard)
    
    @staticmethod
    def create_main_menu_keyboard():
        """Главное меню бота"""
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🍕 Заказать пиццу", "callback_data": "menu_order"},
                    {"text": "📖 Помощь", "callback_data": "menu_help"}
                ]
            ]
        }
        return json.dumps(keyboard)