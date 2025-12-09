import telebot

menu_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
menu_keyboard.add(
    telebot.types.InlineKeyboardButton(text='👤 Профиль', callback_data='profile'),
    telebot.types.InlineKeyboardButton(text='📚 Каталог', callback_data='catalog'),
    telebot.types.InlineKeyboardButton(text='🛒 Корзина', callback_data='cart'),
    telebot.types.InlineKeyboardButton(text='💳 Баланс', callback_data='balance'),
    telebot.types.InlineKeyboardButton(text='💬 Написать в поддержку', url='https://t.me/jowargi')
)

menu_return_keyboard = telebot.types.InlineKeyboardMarkup()
menu_return_keyboard.add(
    telebot.types.InlineKeyboardButton(text='🔙 Назад в меню', callback_data='main_menu')
)

balance_keyboard = telebot.types.InlineKeyboardMarkup(row_width=3)
balance_keyboard.add(
    telebot.types.InlineKeyboardButton(text='➕ 100 ₽', callback_data='add_100'),
    telebot.types.InlineKeyboardButton(text='➕ 500 ₽', callback_data='add_500'),
    telebot.types.InlineKeyboardButton(text='➕ 1000 ₽', callback_data='add_1000'),
    telebot.types.InlineKeyboardButton(text='🔙 Назад в меню', callback_data='main_menu')
)

cart_keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
cart_keyboard.add(
    telebot.types.InlineKeyboardButton(text='💳 Оплатить заказ', callback_data='buy'),
    telebot.types.InlineKeyboardButton(text='🗑️ Очистить корзину', callback_data='clear'),
    telebot.types.InlineKeyboardButton(text='🔙 Назад в меню', callback_data='main_menu')
)
