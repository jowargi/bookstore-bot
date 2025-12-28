import telebot
from bot_instance import bot
import dbhelper
import helpers
from keyboards import (
    menu_keyboard,
    menu_return_keyboard,
    balance_keyboard,
    cart_keyboard,
)


@bot.callback_query_handler(
    func=lambda call: call.data in ["profile", "catalog", "cart", "balance"]
)
def menu_handler(call):
    bot.answer_callback_query(call.id)

    user_id = call.from_user.id
    user_data = dbhelper.fetch_data(
        db_path="./db/bookstore.db",
        table_name="users",
        condition_column="id",
        condition_value=user_id,
    )

    f_name = user_data[1]
    l_name = user_data[2]
    username = user_data[3]
    language_code = user_data[4]
    balance = user_data[5]

    f_name, l_name, username, language_code = map(
        lambda item: "не указано" if not item else item,
        [f_name, l_name, username, language_code],
    )

    username = username if username == "не указано" else f"@{username}"
    balance = int(balance) if balance == int(balance) else balance

    if call.data == "profile":
        helpers.update_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            photo_path="./img/profile.jpg",
            caption=f"👤 <b>Ваш профиль</b>\n\n"
            f"🆔 <b>ID:</b> <code>{user_id}</code>\n"
            f"📧 <b>USERNAME:</b> {username}\n"
            f"📛 <b>Имя:</b> {f_name}\n"
            f"📛 <b>Фамилия:</b> {l_name}\n"
            f"🌐 <b>Язык:</b> {language_code}\n\n"
            f"<i>Для изменения данных обратитесь в поддержку</i>",
            parse_mode="html",
            reply_markup=menu_return_keyboard,
        )

    elif call.data == "balance":
        helpers.update_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            photo_path="./img/balance.jpg",
            caption=f"💰 <b>Текущий баланс</b>\n\n"
            f"<code>{balance} ₽</code>\n\n"
            f"<i>Используйте для покупок в магазине</i>",
            parse_mode="html",
            reply_markup=balance_keyboard,
        )

    elif call.data == "catalog":
        catalog_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)

        for book_data in dbhelper.fetch_data(
            db_path="./db/bookstore.db", table_name="books"
        ):
            book_id = book_data[0]
            title = book_data[1]

            catalog_keyboard.add(
                telebot.types.InlineKeyboardButton(text=title, callback_data=book_id)
            )

        else:
            catalog_keyboard.add(
                telebot.types.InlineKeyboardButton(
                    text="🔙 Назад в меню", callback_data="main_menu"
                )
            )

        helpers.update_message_media(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            photo_path="./img/catalog.jpg",
            caption="📚 <b>Книжная полка</b>\n\n"
            "Все книги в одном месте!\n\n"
            "<i>Нажмите на интересующую книгу для подробностей</i>",
            parse_mode="html",
            reply_markup=catalog_keyboard,
        )

    elif call.data == "cart":
        cart = user_data[7]
        total_amount = user_data[8]

        total_amount = (
            int(total_amount) if total_amount == int(total_amount) else total_amount
        )

        cart = cart.split(",")

        del cart[-1]

        caption = ""

        if len(cart) == 0:
            caption = (
                "📦 <b>Ваша корзина пуста</b>\n\n"
                + "Но это легко исправить!\n"
                + "🔍 <i>Перейдите в каталог и добавьте книги</i>"
            )
            reply_markup = menu_keyboard

        else:
            cart_dict = dict()

            for book_id in cart:
                if book_id not in cart_dict:
                    cart_dict[book_id] = 1

                else:
                    cart_dict[book_id] += 1

            for book_id in cart_dict:
                count = cart_dict[book_id]

                book_data = dbhelper.fetch_data(
                    db_path="./db/bookstore.db",
                    table_name="books",
                    condition_column="id",
                    condition_value=book_id,
                )

                _, title, author, price, __, ___ = book_data

                total_price = price * count

                price = int(price) if price == int(price) else price
                total_price = (
                    int(total_price) if total_price == int(total_price) else total_price
                )

                caption += (
                    f"📚 <b>{title}</b>\n"
                    + f"✍️ <b>Автор:</b> {author}\n"
                    + f"💰 <b>Цена:</b> {price} ₽ × {count} = {total_price} ₽\n"
                    + f"📦 <b>Количество:</b> {count} шт.\n\n"
                )

            caption += f"📚 <b>Стоимость всех книг: {total_amount} ₽</b>"
            reply_markup = cart_keyboard

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

        with open(file="./img/cart.jpg", mode="rb") as photo:
            bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=caption,
                parse_mode="html",
                reply_markup=reply_markup,
            )
