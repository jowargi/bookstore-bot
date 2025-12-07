from bot_instance import bot
from keyboards import menu_keyboard


@bot.callback_query_handler(func=lambda call: call.data == 'main_menu')
def menu_return_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

    bot.send_message(
        chat_id=call.message.chat.id,
        text='🔙 <b>Возврат в меню</b>\n\n'
             '<i>Куда отправимся?</i>\n'
             '↓ ↓ ↓',
        parse_mode='html',
        reply_markup=menu_keyboard
    )
