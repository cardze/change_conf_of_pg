from choose_relation_from_query import get_candidates
from config import db_config
from connection import connect, check_table_exist, check_exist
import pandas as pd

if __name__ == "__main__":
    candidates = get_candidates("../input/", ["src", "output", "raw_all_in_sql", "config"])
    sql =[]
    relation = []
    exist = []
    for key,value in candidates.items():
        for cand in value:
            sql.append(key)
            relation.append(cand)
            exist.append(check_exist(cand))
            print("In sql {0} {1} is exist : {2}".format(key, cand, check_exist(cand)))
    data = list(zip(sql, relation, exist))
    output_data = pd.DataFrame(data, columns=["SQL", "Table name", "Exist"])
    output_data.to_csv("../output/check_result.csv")