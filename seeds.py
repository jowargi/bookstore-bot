import dbhelper
import uuid

dbhelper.create_table(
    db_path='./db/bookstore.db',
    table_name='users',
    id='INT',
    f_name='TEXT',
    l_name='TEXT',
    username='TEXT',
    language_code='TEXT',
    balance='REAL',
    book_id='TEXT',
    cart='TEXT',
    total_amount='REAL'
)

dbhelper.create_table(
    db_path='./db/bookstore.db',
    table_name='books',
    id='TEXT',
    title='TEXT',
    author='TEXT',
    price='REAL',
    url='TEXT',
    img='TEXT'
)

dbhelper.insert_row(
    db_path='./db/bookstore.db',
    table_name='books',
    id=str(uuid.uuid4()),
    title='Война и мир',
    author='Лев Николаевич Толстой',
    price=3199.99,
    url='https://ru.wikipedia.org/wiki/Война_и_мир',
    img='war-and-peace.jpg'
)

dbhelper.insert_row(
    db_path='./db/bookstore.db',
    table_name='books',
    id=str(uuid.uuid4()),
    title='Мёртвые души',
    author='Н. В. Гоголь',
    price=579.8,
    url='https://ru.wikipedia.org/wiki/Мёртвые_души',
    img='dead-souls.jpg'
)

dbhelper.insert_row(
    db_path='./db/bookstore.db',
    table_name='books',
    id=str(uuid.uuid4()),
    title='Преступление и наказание',
    author='Фёдор Достоевский',
    price=799,
    url='https://ru.wikipedia.org/wiki/Преступление_и_наказание',
    img='crime-and-punishment.jpg'
)

dbhelper.insert_row(
    db_path='./db/bookstore.db',
    table_name='books',
    id=str(uuid.uuid4()),
    title='Евгений Онегин',
    author='А. С. Пушкин',
    price=749.8,
    url='https://ru.wikipedia.org/wiki/Евгений_Онегин',
    img='eugene-onegin.jpg'
)
