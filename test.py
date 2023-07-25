import psycopg2
import os
import csv
import json
import itertools
import paramiko
import time
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
        # for set in all_set:
        #     for k,v in set.items():
        #         print("{0}='{1}'".format(k, v))
        return all_set
    
def write_file_on_server(file_name, content):
    with paramiko.SSHClient() as client:
        params = db_config(file_path="./config/database.ini", section='server')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**params)
        trans = client.get_transport()
        with paramiko.SFTPClient.from_transport(trans) as sftp:
            stdin , stdout, stderr = client.exec_command("touch {}".format(file_name))
            result = stdout.readlines()
            print(result)
            with sftp.file(file_name, "w") as file:
                file.write(content)
            stdin , stdout, stderr = client.exec_command("cat {}".format(file_name))
            result = stdout.readlines()
            error = stderr.readlines()
            print("result : {0} \n error : {1}".format(result[-3:-1], error))
        stdin , stdout, stderr = client.exec_command("sh restart_postgresql.sh")
        result = stdout.readlines()
        error = stderr.readlines()
        print("result : {0} \n error : {1}".format(result, error))
        
            
def restart_postgresql():
    with paramiko.SSHClient() as client:
        params = db_config(file_path="./config/database.ini", section='server')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**params)
        stdin , stdout, stderr = client.exec_command("systemctl restart postgresql.service", get_pty=True)
        result = stdout.readlines()
        error = stderr.readlines()
        print("result : {0} \n error : {1}".format(result, error))
        if len(error) is not 0:
            # systemctl status postgresql.service
            stdin , stdout, stderr = client.exec_command("systemctl status postgresql.service", get_pty=True)
            result = stdout.readlines()
            print("check : \n ")
            for i in result:
                print(i)
            result = [] # clean the result buffer
            error = stderr.readlines()
            print("result : {0} \n error : {1}".format(result, error))


def change_pg_conf(content):
    write_file_on_server("/var/lib/pgsql/data/postgresql.conf", content=content)
    time.sleep(1)

if __name__ == "__main__":
    file_name = "test.txt"
    ori = ""
    content = ""
    with open("./config/default.conf", "r") as s:
        for i in s.readlines():
            ori+=i
    for set in generate_all_possible_config():
        content = ori
        for k, v in set.items():
            content+="{0}='{1}'\n".format(k, v)
        change_pg_conf(content)

    
