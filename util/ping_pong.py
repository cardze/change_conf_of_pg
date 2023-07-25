import paramiko
from util.config import db_config

if __name__ == "__main__":
    with paramiko.SSHClient() as client:
        params = db_config(section="server")
        client.connect(**params)
        stdin , stdout, stderr = client.exec_command("echo Hello!!")
        result = stdout.readlines()
        print(result)