import paramiko
import time
import util.config

class Server:
    def __init__(self, server_config_path="../config/database.ini") -> None:
        self.client = paramiko.SSHClient()
        self.params = util.config.db_config(server_config_path, section='server')
        self.is_connect = False
    def connect(self):
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(**self.params, timeout=999)
        self.is_connect = True

    def disconnect(self):
        self.client.close()
        self.is_connect = False
        
    def send_cmd(self, cmd:str, verbose=False):
        if self.is_connect == False:
            print("LOCAL : Please do the connection first and don't forget to close it.")
            return "LOCAL : connection error"
        stdin , stdout, stderr = self.client.exec_command(cmd, get_pty=True)
        result = stdout.readlines()
        error = stderr.readlines()
        if verbose:
            print("SERVER : result : {0} \n error : {1}".format(result, error))
        if len(error)>=1:
            print("SERVER : There is some error : {}".format(error))
            return "ERROR"
        return stdin , stdout, stderr

    def send_cmd_channel(self, cmd:str, verbose=False):
        if self.is_connect == False:
            print("LOCAL : Please do the connection first and don't forget to close it.")
            return "LOCAL : connection error"
        trans = self.client.get_transport()
        channel = trans.open_session()
        print("SERVER : executing command", cmd)
        channel.exec_command(cmd)
        error_channel = channel.makefile_stderr()
        output_channel = channel.makefile()
        cmd_err = ""
        cmd_output = ""
        for err in error_channel.read():
            cmd_err += err
        for out in output_channel.read():
            cmd_output+= out
        if len(cmd_err) > 0 :
            print("SERVER ERROR :", cmd_err)
        return cmd_output.splitlines()
    
    def start_record(self):
        print("Start recording by using BCC tools... ")
        print("The record will be store in ~/logs/ folder")
        cmd = "./start_bcc_recording.sh &"
        if self.is_connect == False:
            print("LOCAL : Please do the connection first and don't forget to close it.")
            return "LOCAL : connection error"
        self.send_cmd(cmd=cmd, verbose=True)

    def stop_record(self, store_path:str):
        print("stoping the bcc recording process")
        cmd = "./stop_bcc_recording.sh"
        if self.is_connect == False:
            print("LOCAL : Please do the connection first and don't forget to close it.")
            return "LOCAL : connection error"
        self.send_cmd(cmd=cmd, verbose=True)
        # store the log to local
        with self.client.open_sftp() as sftp:
            sftp.get("logs/ext4slower.log", store_path)




        
