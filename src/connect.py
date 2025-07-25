import pandas as pd
import psycopg2
from psycopg2 import pool
from dotenv import load_dotenv
import os

load_dotenv()

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10,
    user=os.getenv('user'),
    password=os.getenv('password'),
    host=os.getenv('host'),
    port=os.getenv('port'),
    dbname=os.getenv('dbname'),
    sslmode='require'
)

def get_connection():
    return connection_pool.getconn()

def put_connection(conn):
    return connection_pool.putconn(conn)

def close_connection():
    return connection_pool.closeall()

def run_query(sql_query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_query, params)
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                df = pd.DataFrame(rows, columns=columns)
                return df
            else:
                conn.commit()
                return None
    except Exception as e:
        print(f'Error while executing the query: {sql_query}')
        print(e)
    finally:
        put_connection(conn)