import psycopg2
import os
import csv
import json
import itertools
from util.config import db_config
from util.connection import send_query, get_pg_config


def generate_conf_json():
    query = "SHOW all;"
    conf_path = "./config/database.ini"
    params = db_config(conf_path)
    filename = "conf"
    path = "./config/db_conf.json"
    db_config = get_pg_config(params=params)
    with open(path, 'w') as outputFile:
        outputFile.write("{\n")
        for key, value in db_config.items():
            outputFile.writelines("\t\""+str(key)+"\":[\""+str(value)+"\"],\n")
        outputFile.write("}\n")

def dict_product(dicts):
    """
    >>> list(dict_product(dict(number=[1,2], character='ab')))
    [{'character': 'a', 'number': 1},
     {'character': 'a', 'number': 2},
     {'character': 'b', 'number': 1},
     {'character': 'b', 'number': 2}]
    """
    return (dict(zip(dicts, x)) for x in itertools.product(*dicts.values()))

def generate_all_possible_config():
    with open("./config/db_conf.json" , "r") as file:
        my_conf = json.load(file)   
        all_set = dict_product(dict(my_conf)) 
        for set in all_set:
            for k,v in set.items():
                print("{0}='{1}'".format(k, v))

import paramiko
from util.config import db_config

if __name__ == "__main__":
    with paramiko.SSHClient() as client:
        params = db_config(file_path="./config/database.ini", section='server')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**params)
        stdin , stdout, stderr = client.exec_command("echo Hello!!")
        result = stdout.readlines()
        print(result)