
from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Load environment variables
load_dotenv()

# дополнительно создаем для удобного управления миграциями базы данных
def create_tables():
    connection = psycopg2.connect(
        host=os.getenv('FSTR_DB_HOST'),
        port=os.getenv('FSTR_DB_PORT'),
        dbname=os.getenv('FSTR_DB_NAME'),
        user=os.getenv('FSTR_DB_LOGIN'),
        password=os.getenv('FSTR_DB_PASS')
    )
    cursor = connection.cursor()

    cursor.execute('''
        CREATE SEQUENCE IF NOT EXISTS pereval_id_seq;
        CREATE TABLE IF NOT EXISTS public.pereval_added (
            id int4 NOT NULL DEFAULT nextval('pereval_id_seq'::regclass),
            date_added timestamp,
            raw_data json,
            images json,
            status varchar(20) NOT NULL DEFAULT 'new',
            PRIMARY KEY (id)
        );

        CREATE SEQUENCE IF NOT EXISTS pereval_areas_id_seq;
        CREATE TABLE IF NOT EXISTS public.pereval_areas (
            id int8 NOT NULL DEFAULT nextval('pereval_areas_id_seq'::regclass),
            id_parent int8 NOT NULL,
            title text,
            PRIMARY KEY (id)
        );

        CREATE SEQUENCE IF NOT EXISTS pereval_images_id_seq;
        CREATE TABLE IF NOT EXISTS public.pereval_images (
            id int4 NOT NULL DEFAULT nextval('pereval_images_id_seq'::regclass),
            date_added timestamp DEFAULT now(),
            img bytea NOT NULL,
            PRIMARY KEY (id)
        );

        CREATE SEQUENCE IF NOT EXISTS untitled_table_200_id_seq;
        CREATE TABLE IF NOT EXISTS public.spr_activities_types (
            id int4 NOT NULL DEFAULT nextval('untitled_table_200_id_seq'::regclass),
            title text,
            PRIMARY KEY (id)
        );
    ''')

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    create_tables()

    #Обновление DatabaseHandler после REST API
class DatabaseHandler:
    def __init__(self):
        self.host = os.getenv('FSTR_DB_HOST')
        self.port = os.getenv('FSTR_DB_PORT')
        self.user = os.getenv('FSTR_DB_LOGIN')
        self.password = os.getenv('FSTR_DB_PASS')
        self.dbname = 'pereval'

        self.connection = psycopg2.connect(
            dbname=self.dbname, user=self.user, password=self.password,
            host=self.host, port=self.port
        )
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    def get_pereval_by_id(self, id):
        query = "SELECT * FROM public.pereval_added WHERE id = %s"
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()

    def update_pereval(self, id, data):
        query = "SELECT status FROM public.pereval_added WHERE id = %s"
        self.cursor.execute(query, (id,))
        status = self.cursor.fetchone()
        if status and status[0] == 'new':
            fields = {k: v for k, v in data.items() if k not in ['fio', 'email', 'phone']}
            set_clause = ', '.join([f"{k} = %s" for k in fields])
            values = list(fields.values())
            values.append(id)
            update_query = f"UPDATE public.pereval_added SET {set_clause} WHERE id = %s"
            self.cursor.execute(update_query, values)
            return 1, "Updated successfully"
        else:
            return 0, "Record not found or not editable"

    def get_perevals_by_email(self, email):
        query = "SELECT * FROM public.pereval_added WHERE email = %s"
        self.cursor.execute(query, (email,))
        return self.cursor.fetchall()


def get_pereval_by_id(self, id):
    with self.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM perevals WHERE id = %s", (id,))
        record = cursor.fetchone()
        if record:
            return {
                'id': record[0],
                'name': record[1],
                'height': record[2],
                'difficulty': record[3],
                'user_email': record[4]
            }
        return None


def update_pereval(self, id, data):
    update_fields = []
    update_values = []
    allowed_fields = ['name', 'height', 'difficulty']

    for key, value in data.items():
        if key in allowed_fields:
            update_fields.append(f"{key} = %s")
            update_values.append(value)

    if not update_fields:
        return 0, "No valid fields to update"

    update_values.append(id)

    query = f"UPDATE perevals SET {', '.join(update_fields)} WHERE id = %s"

    with self.connection.cursor() as cursor:
        cursor.execute(query, update_values)
        return 1, "Update successful"


def get_perevals_by_email(self, email):
    with self.connection.cursor() as cursor:
        cursor.execute("SELECT * FROM perevals WHERE user_email = %s", (email,))
        records = cursor.fetchall()
        return [
            {
                'id': record[0],
                'name': record[1],
                'height': record[2],
                'difficulty': record[3],
                'user_email': record[4]
            } for record in records
        ]