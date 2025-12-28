from bot_instance import bot
import dbhelper
from keyboards import menu_keyboard, balance_keyboard


@bot.callback_query_handler(func=lambda call: call.data in ["buy", "clear"])
def cart_action_handler(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

    user_id = call.from_user.id
    user_data = dbhelper.fetch_data(
        db_path="./db/bookstore.db",
        table_name="users",
        condition_column="id",
        condition_value=user_id,
    )

    balance = user_data[5]
    total_amount = user_data[8]

    if call.data == "clear":
        dbhelper.update_row(
            db_path="./db/bookstore.db",
            table_name="users",
            condition_column="id",
            condition_value=user_id,
            cart="",
            total_amount=0,
        )

        bot.send_message(
            chat_id=call.message.chat.id,
            text="🗑️ <b>Корзина очищена!</b>\n\n"
            "🛍️ Все товары удалены из корзины.\n\n"
            "<i>Выберите следующий шаг в меню ↓</i>",
            parse_mode="html",
            reply_markup=menu_keyboard,
        )

    elif call.data == "buy":
        if balance < total_amount:
            bot.send_message(
                chat_id=call.message.chat.id,
                text="❌ <b>Недостаточно средств!</b>\n\n"
                "💰 Вашего баланса не хватает для оплаты заказа.\n\n"
                "<i>Пополните баланс или измените заказ</i>",
                parse_mode="html",
                reply_markup=balance_keyboard,
            )

        else:
            dbhelper.update_row(
                db_path="./db/bookstore.db",
                table_name="users",
                condition_column="id",
                condition_value=user_id,
                balance=balance - total_amount,
                cart="",
                total_amount=0,
            )

            bot.send_message(
                chat_id=call.message.chat.id,
                text="💰 <b>Платёж получен!</b>\n\n"
                "📦 <i>Ваш заказ оформлен.</i>\n"
                "Мы уведомим вас о статусе доставки.\n\n"
                "✨ Спасибо за покупку!",
                parse_mode="html",
                reply_markup=menu_keyboard,
            )
