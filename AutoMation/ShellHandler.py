import paramiko
import time
import re
import datetime

class ShellHandler:
    def __init__(self,):
        self.ssh = paramiko.SSHClient()

    def __del__(self):
        self.ssh.close()

    def login_host(self, host, user, psw):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=user, password=psw, port=22)
    
    def logout_host(self):
        self.ssh.close()
        
    def execute_some_command(self, cmd):
        self.ssh_stdin, self.ssh_stdout, self.ssh_stderr = self.ssh.exec_command(cmd)
        sshname = datetime.datetime.now().strftime('sshmessage_%m%d%H.log')  
        log = str(self.ssh_stdout.read())
        sshmessage = open(sshname+".txt", "a")
        sshmessage.write(log)
        sshmessage.close()
        return (log)  
        
         
        
