from choose_relation_from_query import get_candidates
from config import db_config
from connection import connect, check_table_exist, check_exist, send_query
import pandas as pd
import os
import time

if __name__ == "__main__":
    root_path = '../input/test'
    query_list = os.listdir(root_path)
    for query_file in query_list:
        with open(root_path+"/"+query_file, 'r') as file:
            query = file.read()
            send_query(query=query, save_to=str(query_file), verbose=True)
            print(str(query_file), "is send to the server.")
            time.sleep(3)