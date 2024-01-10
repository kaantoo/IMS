import psycopg2

def create_connection():
    # Replace these with your PostgreSQL database information
    db_name = 'Ims'
    db_user = 'postgres'
    db_password = '8516'
    db_host = 'localhost'
    db_port = '5432'

    try:
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        return conn

    except (Exception, psycopg2.Error) as error:
        print(f"Error connecting to PostgreSQL: {error}")
        return None

def close_connection(conn):
    if conn:
        conn.close()
