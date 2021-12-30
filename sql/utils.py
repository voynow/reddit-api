import psycopg2
from sqlalchemy import create_engine

from config import get_password


def db_init():

    # retrieve password
    password = get_password()

    # create sqlalchemy engine
    engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/financial_data')

    # Connect to postgres financial_data database
    con = psycopg2.connect(
                host="localhost",
                database="reddit_api",
                user='postgres',
                password=f'{password}')

    return con, engine
