import psycopg2
from util.config import db_config
import os
import csv

            # centos() / postgresql (here!)

class Connection:
    def __init__(self, params:dict, query:str) -> None:
        self.connect = psycopg2.connect(**params)
        self.query = query
        self.connect.autocommit = True
        self.planning = None
        self.prepared = "PREPARE" in self.query

    def get_pid(self):
        with self.connect.cursor() as cur:
            # do the checking
            cur.execute("select pg_backend_pid();")
            ret = cur.fetchall()
            return ret[0][0]

    def get_explain_of_query(self):
        explain_prefix = "EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)\n"
        ready_query = explain_prefix+self.query
        with self.connect.cursor() as cur:
            if self.prepared :
                pre_stmt = self.query.split("EXECUTE")[0] + "\n"
                cur.execute(pre_stmt)
                exe_query = "EXECUTE "+self.query.split("EXECUTE")[1]
                ready_query = explain_prefix+exe_query
                # actually call five time
                # for i in range(5):
                #     cur.execute(exe_query)
            cur.execute(ready_query)
            ret = cur.fetchall()
            self.planning = ret[0][0][0]
            return ret[0][0][0]

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

# developing
def send_query_explain_with_prepared_stmt(params:dict, query:str):
    pre_stmt = query.split("EXECUTE")[0]
    exe_query = query.split("EXECUTE")[1]

    explain_query = "EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)\n EXECUTE "+exe_query

    with psycopg2.connect(**params) as conn:
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        cur.execute(pre_stmt+explain_query)
        ret = cur.fetchall()
        # for i in cur.fetchall():
        #     ret+=i
        # print(ret[0][0][0])
        return ret[0][0][0] # json format
