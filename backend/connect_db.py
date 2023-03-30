import psycopg2

def db_connection():
    # Update [DBNAME] and [PASSWORD]
    return psycopg2.connect("dbname=[DBNAME] user=postgres password=[PASSWORD]")