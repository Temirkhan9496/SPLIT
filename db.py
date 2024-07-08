import psycopg2
from dotenv import load_dotenv
import os

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