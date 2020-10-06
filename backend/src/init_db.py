import pandas as pd
import mysql.connector
from mysql.connector.errors import InterfaceError
from sqlalchemy import types, create_engine
import logging

logging.basicConfig(level=logging.INFO)

from lib.museum_wiki_db import generate_museum_db_to_csv, generate_full_museum_df

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    from time import sleep
    # Wait some time so that MySQL server starts
    sleep(10)
    # MySQL Connection
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = open('/run/secrets/db-password').read().strip()
    MYSQL_HOST = 'db'
    MYSQL_PORT = 3306
    MYSQL_DATABASE = 'example'

    engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}', echo=False)

    try:
        connection = engine.connect()
    except InterfaceError as e:
        print('DB unreachable, waiting ...')
        sleep(30)
        connection = engine.connect()

    
    connection.execute('DROP TABLE IF EXISTS museums;')

    df = generate_full_museum_df()
    print('Prepared data:')
    print(df)

    frame = df.to_sql('museums', con=engine, if_exists='append')
    connection.close()
