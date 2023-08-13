import psycopg2
import os
import csv
import json
import itertools
import paramiko
import time
from util.config import db_config
from util.connection import send_query, get_pg_config, send_query_explain


def generate_conf_json():
    query = "SHOW all;"
    conf_path = "./config/database.ini"
    params = db_config(conf_path)
    filename = "conf"
    path = "./config/db_conf.json"
    db_config_dict = get_pg_config(params=params)
    with open(path, 'w') as outputFile:
        outputFile.write("{\n")
        for key, value in db_config_dict.items():
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
    restart_postgresql()
        
            
def restart_postgresql():
    with paramiko.SSHClient() as client:
        params = db_config(file_path="./config/database.ini", section='server')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**params)
        stdin , stdout, stderr = client.exec_command("systemctl restart postgresql.service", get_pty=True)
        result = stdout.readlines()
        error = stderr.readlines()
        print("result : {0} \n error : {1}".format(result, error))
        if len(error) > 0:
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

def get_sql_content(path):
    ret = ""
    with open(path, "r") as file:
        for i in file.readlines():
            ret+=i
        return ret

def get_sql_list(from_here):
    tmp_dct = {}
    for query in os.listdir(from_here):
        tmp_dct[query] = get_sql_content(from_here+"/"+query)
    return tmp_dct

def clean_cache():
    with paramiko.SSHClient() as client:
        params = db_config(file_path="./config/database.ini", section='server')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**params)
        stdin , stdout, stderr = client.exec_command("sh clean_pg_cache.sh", get_pty=True)
        result = stdout.readlines()
        error = stderr.readlines()
        print("result : {0} \n error : {1}".format(result, error))

def wait_for_cpu():
    with paramiko.SSHClient() as client:
        params = db_config(file_path="./config/database.ini", section='server')
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(**params, timeout=999)
        CPU_st = []
        while True:
            stdin , stdout, stderr = client.exec_command("sar -u 1 1 | awk '/^Average:/{print 100-$8}'", get_pty=True)
            result = stdout.readlines()
            error = stderr.readlines()
            print("result : {0} \n error : {1}".format(result, error))
            CPU_st.append(float(result[0]))
            if len(CPU_st) > 3:
                CPU_st.pop(0)
            if len(CPU_st) == 3 :
                print("rest for 3 sec...")
                time.sleep(3)
                for i in range(3):
                    if CPU_st.pop(0) > 5:
                        break
                    return
                

def run_test(cold:bool, iter_time=10):
    report_path = "./report/report_{}".format(time.strftime("%Y-%m-%d-%H%M%S"))
    if os.path.exists(report_path) == False:
        os.mkdir(report_path)
    query_path = "./raw_queries"
    query_dict = {}
    query_dict = get_sql_list(query_path)
    print(query_dict.keys())
    params = db_config("./config/database.ini")
    ori = ""
    content = ""
    with open("./config/default.conf", "r") as s:
        for i in s.readlines():
            ori+=i
    for set in generate_all_possible_config():
        content = ori
        conf_alter = ""
        for k, v in set.items():
            conf_alter+="{0}='{1}'\n".format(k, v)
        content+=conf_alter
        change_pg_conf(content)
        # start sending query
        # need to store explain and conf
        explain = ""
        for k, v in query_dict.items():
            total_time =0
            tmp_folder_name = str(k.split('.')[0])+"tmp"
            small_report_path = report_path+"/"+tmp_folder_name
            if os.path.exists(small_report_path) == False:
                os.mkdir(small_report_path)
            for i in range(iter_time):
                if cold == True : 
                    clean_cache()
                    wait_for_cpu()
                explain = send_query_explain(params, v) # dict
                explain_json = json.dumps(explain)
                print(type(explain_json))
                print(k.split('.')[0], "exec : ",explain['Execution Time'],"ms plan : ", explain['Planning Time'], "ms")
                if i != 0:
                    total_time += int(explain['Execution Time'])+ int(explain['Planning Time'])
                if os.path.exists(small_report_path+"/plan") == False:
                    os.mkdir(small_report_path+"/plan")
                with open(small_report_path+"/plan/"+str(k.split('.')[0])+"_"+str(i)+".json", "w") as plan_file:
                    plan_file.writelines(str(explain_json))    
            total_time/=(iter_time-1)
            folder_name=str(k.split('.')[0])+"_"+str(int(total_time))
            if cold :
                folder_name+="_Cold"
            else:
                folder_name+="_Warm"
            # ensure that the folder won't be renamed to the former iteration
            time.sleep(1)
            os.rename(report_path+"/"+tmp_folder_name, report_path+"/"+folder_name)
            small_report_path = report_path+"/"+folder_name
            if os.path.exists(small_report_path) == False:
                os.mkdir(small_report_path)
            with open(small_report_path+"/conf.conf", "w") as conf_file:
                conf_file.writelines(conf_alter)

if __name__ == "__main__":
    iter_time = 3
    run_test(False, iter_time) # warm
    run_test(True, iter_time)  # cold
    # generate_conf_json()
