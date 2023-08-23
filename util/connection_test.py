import psycopg2
# from util.config import db_config
from config import db_config

import os
import csv


class Connection:
    def __init__(self, params:dict, query:str) -> None:
        self.connect = psycopg2.connect(**params)
        self.query = query
        self.connect.autocommit = True
        self.planning = None

    def get_pid(self):
        with self.connect.cursor() as cur:
            # do the checking
            cur.execute("select pg_backend_pid();")
            ret = cur.fetchall()
            return ret[0][0]

    def get_explain_of_query(self):
        explain_prefix = "EXPLAIN (ANALYZE, COSTS, VERBOSE, BUFFERS, FORMAT JSON)\n"
        with self.connect.cursor() as cur:
            cur.execute(explain_prefix+self.query)
            ret = cur.fetchall()
            self.planning = ret[0][0][0]
            return ret[0][0][0]



if __name__ == "__main__":
    query = "select item_id from dct_items;"
    test_params = db_config("../config/database.ini")
    c = Connection(test_params, query)
    print(c.get_pid())
    print(c.get_explain_of_query())

        