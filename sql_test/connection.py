import psycopg2
from util.config import db_config
import os

def connect():
    conn = None
    try:
        params = db_config()
        print("Connecting...")
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        print("postgresql database version:")
        cur.execute('select version()')
        # display
        db_version = cur.fetchone()
        print(db_version)
        # close communication
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

def send_query(query:str, save_to:str, verbose=True):
    conn = None
    try:
        params = db_config()
        print("Connecting...")
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        # display
        ret_query = cur.fetchall()
        if verbose == True : 
            print(ret_query)
        if os.path.exists("./sql_output") is False:
            os.mkdir("./sql_output")
        print("Writing sql result to", "./sql_output/"+save_to)
        with open("./sql_output/"+save_to, 'w') as outputFile:
            outputFile.write(str(ret_query))
        # close communication
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")

def check_table_exist(table_name):
    conn = None
    ret = False
    try:
        params = db_config()
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute('''SELECT EXISTS (
    SELECT FROM 
        pg_tables
    WHERE 
        schemaname = 'public' AND 
        tablename  = '{0}'
    );'''.format(table_name))
        # display
        existance = cur.fetchone()
        if existance[0] == True:
            ret = True
        # close communication
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return ret

def check_view_exist(view_name):
    conn = None
    ret = False
    try:
        params = db_config()
        conn = psycopg2.connect(**params)
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute('''SELECT EXISTS (
    SELECT FROM 
        pg_views
    WHERE 
        schemaname = 'public' AND 
        viewname  = '{0}'
    );'''.format(view_name))
        # display
        existance = cur.fetchone()
        if existance[0] == True:
            ret = True
        # close communication
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return ret


def check_exist(name):
    if check_table_exist(name):
        return "True"
    if check_view_exist(name):
        return "True"
    return "False"

if __name__ =="__main__":
    connect()
