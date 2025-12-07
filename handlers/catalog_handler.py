import telebot
from bot_instance import bot
import dbhelper


@bot.callback_query_handler(
    func=lambda call: call.data in dbhelper.get_column_values(
        db_path='./db/bookstore.db',
        table_name='books',
        column_index=0
    )
)
def catalog_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

    book_id = call.data
    book_data = dbhelper.fetch_data(
        db_path='./db/bookstore.db',
        table_name='books',
        condition_column='id',
        condition_value=book_id
    )

    title = book_data[1]
    author = book_data[2]
    price = book_data[3]
    url = book_data[4]
    img = book_data[5]

    price = int(price) if price == int(price) else price

    user_id = call.from_user.id
    dbhelper.update_row(
        db_path='./db/bookstore.db',
        table_name='users',
        condition_column='id',
        condition_value=user_id,
        book_id=book_id
    )

    book_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    book_keyboard.add(
        telebot.types.InlineKeyboardButton(text='📖 Описание книги', url=url),
        telebot.types.InlineKeyboardButton(text='🛒 Добавить в корзину', callback_data='to_cart'),
        telebot.types.InlineKeyboardButton(text='🔙 Назад в меню', callback_data='main_menu')
    )

    with open(f'./img/books/{img}', 'rb') as photo:
        bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=f'📚 <b>{title}</b>\n\n'
                    f'✍️ <b>Автор:</b> {author}\n'
                    f'💰 <b>Цена:</b> <code>{price} ₽</code>\n\n'
                    f'<i>Выберите действие с книгой ↓</i>',
            parse_mode='html',
            reply_markup=book_keyboard
        )
