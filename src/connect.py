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


def save_df_to_db_upsert(df, table_name, key_column):
    """
    Sauvegarde les données du DataFrame 'df' dans la table PostgreSQL 'table_name'.
    - Ajoute les colonnes manquantes (type TEXT).
    - Fait un UPSERT (INSERT ... ON CONFLICT UPDATE) sur la clé 'key_column'.
    """

    existing_cols = set()
    try:
        sql_cols = """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name = %s
        """
        df_cols = run_query(sql_cols, (table_name,))
        existing_cols = set(df_cols['column_name'].tolist())
    except Exception as e:
        print(f"Erreur lors de la récupération des colonnes : {e}")
        return

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for col in df.columns:
                if col not in existing_cols:
                    print(f"Ajout de la colonne {col} (type TEXT) dans {table_name}")
                    sql = f'ALTER TABLE {table_name} ADD COLUMN {col} TEXT'
                    cur.execute(sql)
            conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'ajout des colonnes : {e}")
        conn.rollback()
        put_connection(conn)
        return

    try:
        with conn.cursor() as cur:
            cols = df.columns.tolist()
            cols_str = ', '.join(cols)
            placeholders = ', '.join(['%s'] * len(cols))

            update_cols = [col for col in cols if col != key_column]
            update_str = ', '.join([f"{col} = EXCLUDED.{col}" for col in update_cols])

            sql_upsert = f"""
                INSERT INTO {table_name} ({cols_str})
                VALUES ({placeholders})
                ON CONFLICT ({key_column}) DO UPDATE SET
                {update_str}
            """

            for _, row in df.iterrows():
                values = [str(row[col]) if pd.notna(row[col]) else None for col in cols]
                cur.execute(sql_upsert, values)

            conn.commit()
            print(f"Upsert effectué avec succès dans {table_name}")
    except Exception as e:
        print(f"Erreur lors de l'upsert dans la base: {e}")
        conn.rollback()
    finally:
        put_connection(conn)

def save_df_to_db(df, table_name, key_column='*'):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            sql_cols = """
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = 'public'
            """
            cur.execute(sql_cols, (table_name,))
            existing_cols = set([row[0] for row in cur.fetchall()])

            df_cols = set(df.columns.tolist())

            cols_to_drop = existing_cols - df_cols
            for col in cols_to_drop:
                print(f"Dropping column: {col}")
                cur.execute(f'ALTER TABLE "{table_name}" DROP COLUMN "{col}"')

            cols_to_add = df_cols - existing_cols
            for col in cols_to_add:
                print(f"Adding column: {col}")
                cur.execute(f'ALTER TABLE "{table_name}" ADD COLUMN "{col}" TEXT')

            if key_column == '*':
                print(f"Truncating table: {table_name}")
                cur.execute(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE')

                cols = df.columns.tolist()
                cols_str = ', '.join([f'"{col}"' for col in cols])
                placeholders = ', '.join(['%s'] * len(cols))
                sql_insert = f'INSERT INTO "{table_name}" ({cols_str}) VALUES ({placeholders})'

                for _, row in df.iterrows():
                    values = [str(row[col]) if pd.notna(row[col]) else None for col in cols]
                    cur.execute(sql_insert, values)

            else:
                cols = df.columns.tolist()
                cols_str = ', '.join([f'"{col}"' for col in cols])
                placeholders = ', '.join(['%s'] * len(cols))
                update_cols = [col for col in cols if col != key_column]
                update_str = ', '.join([f'"{col}" = EXCLUDED."{col}"' for col in update_cols])
                sql_upsert = f'''
                    INSERT INTO "{table_name}" ({cols_str})
                    VALUES ({placeholders})
                    ON CONFLICT ("{key_column}") DO UPDATE SET {update_str}
                '''
                for _, row in df.iterrows():
                    values = [str(row[col]) if pd.notna(row[col]) else None for col in cols]
                    cur.execute(sql_upsert, values)

            conn.commit()
            print(f"✅ Données sauvegardées dans {table_name}")

    except Exception as e:
        print(f"❌ Erreur dans save_df_to_db: {e}")
        conn.rollback()
    finally:
        put_connection(conn)

