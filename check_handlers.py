import inspect
from handlers import *

def check_handler_signatures():
    print("=== ПРОВЕРКА СИГНАТУР ОБРАБОТЧИКОВ ===")
    
    handlers = [
        DatabaseLogger,
        StartHandler,
        RestartOrderHandler, 
        PizzaNameHandler,
        PizzaSizeHandler,
        DrinkHandler,
        OrderReviewHandler
    ]
    
    for handler_class in handlers:
        print(f"\n🔍 Проверяем {handler_class.__name__}:")
        
        # Проверяем can_handle
        can_handle_sig = inspect.signature(handler_class.can_handle)
        print(f"  can_handle параметры: {list(can_handle_sig.parameters.keys())}")
        
        # Проверяем handle  
        handle_sig = inspect.signature(handler_class.handle)
        print(f"  handle параметры: {list(handle_sig.parameters.keys())}")
        
        expected_can_handle = ['self', 'update', 'state']
        expected_handle = ['self', 'update', 'db', 'state', 'order_json']
        
        can_handle_params = list(can_handle_sig.parameters.keys())
        handle_params = list(handle_sig.parameters.keys())
        
        if can_handle_params == expected_can_handle:
            print("  ✅ can_handle: OK")
        else:
            print(f"  ❌ can_handle: ожидалось {expected_can_handle}, получено {can_handle_params}")
            
        if handle_params == expected_handle:
            print("  ✅ handle: OK")
        else:
            print(f"  ❌ handle: ожидалось {expected_handle}, получено {handle_params}")

if __name__ == "__main__":
    check_handler_signatures()