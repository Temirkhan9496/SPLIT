from psycopg2 import connect, sql
from psycopg2.extras import Json
from dotenv import load_dotenv
import os

# Загружаем переменные
load_dotenv()

class PerevalDataHandler:
    def __init__(self):
        self.connection = connect(
            host=os.getenv('FSTR_DB_HOST'),
            port=os.getenv('FSTR_DB_PORT'),
            dbname=os.getenv('FSTR_DB_NAME'),
            user=os.getenv('FSTR_DB_LOGIN'),
            password=os.getenv('FSTR_DB_PASS')
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def add_pereval(self, date_added, raw_data, images):
        insert_query = sql.SQL('''
            INSERT INTO public.pereval_added (date_added, raw_data, images, status)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
        ''')
        self.cursor.execute(insert_query, (date_added, Json(raw_data), Json(images), 'new'))
        return self.cursor.fetchone()[0]

    def add_image(self, img):
        insert_query = sql.SQL('''
            INSERT INTO public.pereval_images (img)
            VALUES (%s)
            RETURNING id;
        ''')
        self.cursor.execute(insert_query, (img,))
        return self.cursor.fetchone()[0]

    def __del__(self):
        self.cursor.close()
        self.connection.close()

