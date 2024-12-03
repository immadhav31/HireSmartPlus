import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="resume_scanner",
        user="postgres",
        password="madhav",
        host="localhost",
        port="5432"
    )