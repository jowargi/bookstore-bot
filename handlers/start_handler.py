from bot_instance import bot
import dbhelper
from keyboards import menu_keyboard


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    username = message.from_user.username
    language_code = message.from_user.language_code

    if not dbhelper.fetch_data(
            db_path='./db/bookstore.db',
            table_name='users',
            condition_column='id',
            condition_value=user_id
    ):
        dbhelper.insert_row(
            db_path='./db/bookstore.db',
            table_name='users',
            id=user_id,
            f_name=f_name,
            l_name=l_name,
            username=username,
            language_code=language_code,
            balance=0,
            book_id='',
            cart='',
            total_amount=0
        )

    with open('./img/start.jpg', 'rb') as photo:
        bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption='<b>📚 Добро пожаловать в «bookstore»!</b>\n\n'
                    '<i>Здесь каждая книга — целый мир, а каждый читатель — желанный гость.</i>\n\n'
                    'Мы поможем вам:\n'
                    '• <b>Найти новинки и бестселлеры</b>\n'
                    '• <u>Открыть для себя редкие издания</u>\n'
                    '• <code>Подобрать книгу</code> по настроению или совету\n\n'
                    '<b>Используйте меню ниже</b>, чтобы начать путешествие по страницам!',
            parse_mode='html',
            reply_markup=menu_keyboard
        )
