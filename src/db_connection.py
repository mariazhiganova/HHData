import psycopg2


def create_db(params, db_name):
    try:
        conn = psycopg2.connect(**params)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(f"CREATE DATABASE {db_name};")

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


def create_employers_table(params, db_name):
    params['database'] = db_name
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS employers (
                        id SERIAL PRIMARY KEY,
                        employer_id VARCHAR UNIQUE,
                        name VARCHAR NOT NULL,
                        url VARCHAR,
                        open_vacancies INTEGER
                    );
                ''')
                conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def create_vacancies_table(params, db_name):
    params['database'] = db_name
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute('''
                    CREATE TABLE IF NOT EXISTS vacancies (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR NOT NULL,
                        description TEXT,
                        salary INTEGER NOT NULL,
                        published_at DATE,
                        employer_id VARCHAR NOT NULL,
                        CONSTRAINT fk_employer_id FOREIGN KEY(employer_id) REFERENCES employers(employer_id) ON DELETE CASCADE,
                        url VARCHAR NOT NULL
                    );
                ''')
                conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при создании таблицы: {e}")


def insert_data_in_vacancies(params, db_name, data):
    params['database'] = db_name
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                for v in data:
                    cur.execute('''INSERT INTO vacancies (id, name, description, salary, published_at, employer_id, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        v["id"], v["name"], v["responsibility"], v["salary"]["from"], v["published_at"],
                        v["employer"]["id"]), v['alternate_url'])
                conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при заполнении таблицы: {e}")


def insert_data_in_employers(params, db_name, data):
    params['database'] = db_name
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                for employer_id, employer_info in data.items():
                    if isinstance(employer_info, dict) and employer_info:  # Проверяем тип данных и непустоту
                        open_vacancies = employer_info.get("open_vacancies", 0)
                        name = employer_info.get("name", "Неизвестно")  # Указываем значение по умолчанию
                        url = employer_info.get("url", "")  # URL может быть пустым

                        cur.execute('''INSERT INTO employers (employer_id, name, url, open_vacancies)
                                       VALUES (%s, %s, %s, %s)
                                       ''', (employer_id, name, url, open_vacancies))
                    else:
                        print(f"Неверный формат данных для работодателя {employer_id}: {employer_info}")
                conn.commit()

    except psycopg2.Error as e:
        print(f"Ошибка при заполнении таблицы: {e}")
