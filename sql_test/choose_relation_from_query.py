import os

def split_more_token(input_list, delimeter):
    tmp = []
    for i in input_list:
        tmp+=i.split(delimeter)
    return tmp

def used_table(file_path):
    with open(file_path, 'r') as test:
        ctx = test.read()
        tokens = ctx.split()
        tokens = split_more_token(tokens, '(')
        tokens = split_more_token(tokens, ')')
        tokens = split_more_token(tokens, ',')
        tokens = split_more_token(tokens, 'crosstab')
        # tokens = split_more_token(tokens, '"')
        candidates = []
        for i in range(len(tokens)):
            if tokens[i].lower() in ['from', 'join']:
                candidates.append(tokens[i+1])
        # remove " char
        candidates = [x.replace('\"', '') for x in candidates]
        # dedupe the list
        candidates = list(dict.fromkeys(candidates))
        # remove the empty ele
        candidates = [x for x in candidates if x!=""]
        return candidates

def get_candidates(root, ignore_dir:list):
    candidates_dict = {}
    dir_list = os.listdir(root)
    for i in dir_list:    
        if i not in ignore_dir:
            sql_list = os.listdir(root+i)
            file_dir = root+i+'/'
            for j in sql_list:
                candidates_dict[j]=used_table(file_dir+j)
    # dedupe the list
    for key in candidates_dict:
        candidates_dict[key] = list(dict.fromkeys(candidates_dict[key]))
    return candidates_dict

if __name__=="__main__":
    test = get_candidates("../", ["src", "output", "raw_all_in_sql", "config"])
    for item in test.items():
        print(item)


# candidates_list = []
# dir_list = os.listdir('../')
# for i in dir_list:    
#     if i not in ["src", "output", "raw_all_in_sql"]:
#         sql_list = os.listdir('../'+i)
#         # print(sql_list)
#         file_dir = '../'+i+'/'
#         for j in sql_list:
#             candidates_list+=used_table(file_dir+j)
# # dedupe the list
# candidates_list = list(dict.fromkeys(candidates_list))

# for ele in candidates_list:
#     print(ele)