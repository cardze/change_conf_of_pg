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

def send_query_explain(params:dict, query:str):
    explain_query = "EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)\n"+query
    with psycopg2.connect(**params) as conn:
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(explain_query)
        ret = cur.fetchall()
        # for i in cur.fetchall():
        #     ret+=i
        # print(ret[0][0][0])
        return ret[0][0][0] # json format

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
