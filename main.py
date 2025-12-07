from bot_instance import bot
import handlers.start_handler
import handlers.menu_handler
import handlers.menu_return_handler
import handlers.balance_handler
import handlers.catalog_handler
import handlers.to_cart_handler
import handlers.cart_action_handler

while True:
    try:
        bot.polling(none_stop=True, interval=0)

    except Exception as exception:
        print(exception)
