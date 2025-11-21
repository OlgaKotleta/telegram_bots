from enum import Enum

class UserState(Enum):
    """Состояния пользователя в процессе заказа"""
    START = "START"
    WAIT_FOR_PIZZA_NAME = "WAIT_FOR_PIZZA_NAME"
    WAIT_FOR_PIZZA_SIZE = "WAIT_FOR_PIZZA_SIZE"
    WAIT_FOR_DRINKS = "WAIT_FOR_DRINKS"
    WAIT_FOR_ORDER_APPROVE = "WAIT_FOR_ORDER_APPROVE"
    ORDER_FINISHED = "ORDER_FINISHED"