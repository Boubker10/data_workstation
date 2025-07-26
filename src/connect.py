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


def create_table(sql_query):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql_query)
            conn.commit()
    except Exception as e:
        print(f"Erreur lors de la création de table avec : {sql_query}")
        print(e)
    finally:
        put_connection(conn)



def create_table_from_dataframe(df, table_name):
    import numpy as np
    import psycopg2

    type_mapping = {
        'object': 'TEXT',
        'int64': 'BIGINT',
        'float64': 'DOUBLE PRECISION',
        'bool': 'BOOLEAN',
        'datetime64[ns]': 'TIMESTAMP',
        'timedelta[ns]': 'INTERVAL'
    }

    columns_sql = []
    for col in df.columns:
        dtype = str(df[col].dtype)
        pg_type = type_mapping.get(dtype, 'TEXT')  
        columns_sql.append(f'"{col}" {pg_type}')

    columns_def = ',\n  '.join(columns_sql)
    create_table_sql = f"""
    CREATE TABLE {table_name} (
      {columns_def}
    );
    """

    try:
        create_table(create_table_sql)
        print(f"La table '{table_name}' a été créée avec succès.")
    except psycopg2.errors.DuplicateTable:
        print(f"La table '{table_name}' existe déjà.")
    except Exception as e:
        print(f"Erreur lors de la création de la table '{table_name}': {e}")



def insert_dataframe(df, table_name):

    if df.empty:
        print("Le DataFrame est vide. Aucune donnée insérée.")
        return

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cols = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            insert_query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

            data = [tuple(row) for row in df.to_numpy()]
            cur.executemany(insert_query, data)
            conn.commit()
            print(f"{cur.rowcount} lignes insérées dans {table_name}.")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans {table_name}")
        print(e)
    finally:
        put_connection(conn)


