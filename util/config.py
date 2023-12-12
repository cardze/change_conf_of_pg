from configparser import ConfigParser
import pytest

def db_config(file_path='../config/database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read conf file
    parser.read(file_path)
    # get section, default to postgresql
    db = {} # dict
    if parser.has_section(section=section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("SECTION {0} NOT FOUND in the {1} file.".format(section, file_path))

    return db #dict

def test_db_config():
    test_db = db_config("../config/database_test.ini")
    assert test_db["host"] == "127.0.0.1"


if __name__ == '__main__':
    print(db_config())
    # test_db_config()
    # test = db_config()
    # function(**test) # ** is to use dictionary as the function's params
    