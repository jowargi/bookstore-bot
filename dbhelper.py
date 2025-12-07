import sqlite3


def create_table(db_path, table_name, **columns):
    columns_definitions = []
    first_col = True

    for col_name, col_type in columns.items():
        if first_col:
            columns_definitions.append(f"{col_name} {col_type} PRIMARY KEY")
            first_col = False
        else:
            columns_definitions.append(f"{col_name} {col_type}")

    columns_sql = ', '.join(columns_definitions)

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name}({columns_sql})')
        conn.commit()


def insert_row(db_path, table_name, **values):
    placeholders = ', '.join(['?'] * len(values))
    columns = ', '.join(values.keys())
    params = list(values.values())

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'INSERT INTO {table_name}({columns}) VALUES({placeholders})', params)
        conn.commit()


def update_row(db_path, table_name, condition_column, condition_value, **updates):
    set_clause = ', '.join([f"{col} = ?" for col in updates.keys()])
    params = list(updates.values()) + [condition_value]

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f'UPDATE {table_name} SET {set_clause} WHERE {condition_column} = ?', params)
        conn.commit()


def fetch_data(db_path, table_name, condition_column=None, condition_value=None, limit=None):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        if condition_column and condition_value:
            cursor.execute(f'SELECT * FROM {table_name} WHERE {condition_column} = ?', (condition_value,))
            return cursor.fetchone()
        elif limit:
            cursor.execute(f'SELECT * FROM {table_name} LIMIT ?', (limit,))
            return cursor.fetchmany(limit)
        else:
            cursor.execute(f'SELECT * FROM {table_name}')
            return cursor.fetchall()


def delete_rows(db_path, table_name, condition_column=None, condition_value=None):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        if condition_column and condition_value:
            cursor.execute(f'DELETE FROM {table_name} WHERE {condition_column} = ?', (condition_value,))
        else:
            cursor.execute(f'DELETE FROM {table_name}')

        conn.commit()


def get_table_names(db_path):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return [row[0] for row in cursor.fetchall()]


def get_column_values(db_path, table_name, column_index):
    data = fetch_data(db_path, table_name)
    return [row[column_index] for row in data] if data else []
