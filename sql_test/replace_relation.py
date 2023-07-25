import os

replace_list = [
    {
        'from':'dct_ticket_fields',
        'to':'dct_cmdb_data_fields'
    }, 
    {
        'from':'''item0_3_."switch_item_id"''',
        'to':'''item0_3_."belongs_to_item_id"'''
    },
    {
        'from':") THEN ''",
        'to':") THEN 0"
    },
    {
        'from':'''cabinetite0_1_."power_panels_count"''',
        'to':'''cabinetite0_1_."num_ports"'''
    },
    {
        'from':'''item0_."power_panels_count"''',
        'to':'''item0_."num_ports"'''
    },
    {
        'from':'''WHEN "TABLE_ME_ITEMS"."batt_string_redundancy" = 0 THEN 'N'
    ELSE ('N+' || CAST("TABLE_ME_ITEMS"."batt_string_redundancy" AS varchar))''',
        'to':'''--WHEN "TABLE_ME_ITEMS"."batt_string_redundancy" = 0 THEN 'N'
    ELSE "TABLE_ME_ITEMS"."batt_string_redundancy"'''
    },
    {
        'from':'''meitem0_1_."power_panels_count"''',
        'to':'''meitem0_1_."num_ports"'''
    },
    {
        'from':'''this_."power_panels_count"''',
        'to':'''this_."num_ports"'''
    },
    {
        'from':'''cracnwgrpi8_."power_panels_count"''',
        'to':'''cracnwgrpi8_."num_ports"'''
    },
    {
        'from':'''parentitem25_."power_panels_count"''',
        'to':'''parentitem25_."num_ports"'''
    },
    {
        'from':'''bladechass6_."power_panels_count"''',
        'to':'''bladechass6_."num_ports"'''
    },
    {
        'from':'''pdupanelit31_."power_panels_count"''',
        'to':'''pdupanelit31_."num_ports"'''
    },
    {
        'from':'''childitems0_."power_panels_count"''',
        'to':'''childitems0_."num_ports"'''
    }
]

def replace_SQL_relation_name(file_path):
    with open(file_path, "r") as input_file:
        ctx = input_file.read()
        for i in replace_list:
            ctx = ctx.replace(i['from'], i['to'])
        return ctx

if __name__ =="__main__":
    input_dir = "../input/"
    dir_list = os.listdir(input_dir)
    print(dir_list)
    output_dir = "../output"
    # make output dir
    if os.path.exists(output_dir) is False:
        os.mkdir(output_dir)
    for i in dir_list:    
        if os.path.exists(output_dir+"/"+i) is False:
            os.mkdir(output_dir+"/"+i)
            print("make dir : ", output_dir+"/"+i)
        sql_list = os.listdir(input_dir+i)
        print(sql_list)
        for j in sql_list:
            with open(output_dir+"/"+i+'/'+j, 'w') as output_file:
                new_sql = replace_SQL_relation_name(input_dir+i+"/"+j)
                output_file.write(new_sql)
