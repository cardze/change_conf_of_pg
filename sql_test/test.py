from choose_relation_from_query import get_candidates
from config import db_config
from connection import connect, check_table_exist, check_exist, send_query
import pandas as pd
import os
import time

def split_sql(source_path, output_path):
    if os.path.exists(output_path) is False:
        os.mkdir(output_path)
    query_list = os.listdir(source_path)
    for query_file in query_list:
        with open(source_path+"/"+query_file, 'r') as file:
            query = file.read()
            query+=';'
            print(len(query.split(';')))
            iter = 0
            file_name = query_file.split('.')[0]
            extension = query_file.split('.')[1]
            for sql in query.split(';'):
                if os.path.exists(output_path+"/"+file_name) is False:
                    os.mkdir(output_path+"/"+file_name)
                if len(sql) == 0 : continue
                iter+=1
                print("output to file at "+output_path+"/"+file_name+"/"+file_name+"_"+str(iter)+"."+extension)
                with open(output_path+"/"+file_name+"/"+file_name+"_"+str(iter)+"."+extension, "w") as output_file:
                    output_file.write(str(sql)+";")



if __name__ == "__main__":
    root_path = '../input/raw_sql_Q'
    out_path = '../output/splited_sql'
    split_sql(root_path, out_path)