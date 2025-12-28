from bot_instance import bot
import dbhelper
from keyboards import menu_keyboard


@bot.callback_query_handler(func=lambda call: call.data == "to_cart")
def to_cart_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

    user_id = call.from_user.id
    user_data = dbhelper.fetch_data(
        db_path="./db/bookstore.db",
        table_name="users",
        condition_column="id",
        condition_value=user_id,
    )

    cart = user_data[7]
    total_amount = user_data[8]

    book_id = user_data[6]
    book_data = dbhelper.fetch_data(
        db_path="./db/bookstore.db",
        table_name="books",
        condition_column="id",
        condition_value=book_id,
    )

    price = book_data[3]

    dbhelper.update_row(
        db_path="./db/bookstore.db",
        table_name="users",
        condition_column="id",
        condition_value=user_id,
        cart=cart + book_id + ",",
        total_amount=total_amount + price,
    )

    bot.send_message(
        chat_id=call.message.chat.id,
        text="📚 <b>Книга добавлена в корзину!</b>\n\n"
        "Теперь она ждёт вас вместе с другими выбранными книгами.\n\n"
        "✨ <i>Что дальше?</i>",
        parse_mode="html",
        reply_markup=menu_keyboard,
    )
