import psycopg2
from util.config import db_config
import os
import csv


def send_query(params:dict, query:str, output_filename:str):
    saved_path = ["sql_output", output_filename]
    ext = ".csv"
    with psycopg2.connect(**params) as conn:
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        ret_query = cur.fetchall()
        if os.path.exists("./"+saved_path[0]) is False:
            os.mkdir("./"+saved_path[0])
        path = "."
        for i in saved_path:
            path += ("/"+i)
        path+=ext
        print("Writing sql result to", path)
        with open(path, 'w') as outputFile:
            writer = csv.writer(outputFile, delimiter=',')
            writer.writerow([x[0] for x in cur.description])
            for row in ret_query:
                writer.writerow(row)

def get_pg_config(params:dict):
    query = "show all;"
    with psycopg2.connect(**params) as conn:
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(query)
        ret_query = cur.fetchall()
        new_ret = [[x[0],x[1]] for x in ret_query]
        return dict(new_ret)
