import psycopg2
from config import db_host,db_name,db_password,db_user


def connect_to_server(): 
    try:
        con = psycopg2.connect(
            host=db_host, 
            database=db_name, 
            user=db_user, 
            password=db_password,
            port='5432'  # as usual
        )
        cursor = con.cursor()
        print("Подключение к серверу прошло успешно")
        cursor.execute("CREATE TABLE IF NOT EXISTS people (id SERIAL PRIMARY KEY, user_id BIGINT UNIQUE);")
        cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    users_id BIGINT,
                    description TEXT,
                    FOREIGN KEY (users_id) REFERENCES people(user_id) ON DELETE CASCADE)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS feedbacks2 (
                    id SERIAL PRIMARY KEY,
                    text TEXT,
                    date TEXT)""")
        return con, cursor
    except Exception as error:
        print("Подключение к серверу не удалось: ", error)




