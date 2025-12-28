from bot_instance import bot
import dbhelper
from keyboards import menu_keyboard


@bot.callback_query_handler(
    func=lambda call: call.data in ["add_100", "add_500", "add_1000"]
)
def balance_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

    user_id = call.from_user.id
    user_data = dbhelper.fetch_data(
        db_path="./db/bookstore.db",
        table_name="users",
        condition_column="id",
        condition_value=user_id,
    )

    balance = user_data[5]
    replenishment_amount = float(call.data[4:])
    replenishment_amount = (
        int(replenishment_amount)
        if replenishment_amount == int(replenishment_amount)
        else replenishment_amount
    )

    dbhelper.update_row(
        db_path="./db/bookstore.db",
        table_name="users",
        condition_column="id",
        condition_value=user_id,
        balance=balance + replenishment_amount,
    )

    bot.send_message(
        chat_id=call.message.chat.id,
        text=f"💰 <b>Пополнение принято!</b>\n\n"
        f"На ваш счёт добавлено <u>{replenishment_amount} ₽</u>\n\n"
        f"<i>Теперь можно выбрать новые книги!</i>",
        parse_mode="html",
        reply_markup=menu_keyboard,
    )
