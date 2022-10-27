import ShellHandler
import sys
ssh = ShellHandler.ShellHandler()
def link_drop_init():
    ssh.login_host(host = "192.168.88.81", user = "root", psw = "12345678")
    ssh.execute_some_command('python3 /home/hpa/Desktop/ras_pi/script/link/link_drop_init.py')
    ssh.execute_some_command('exit')
    ssh.login_host(host = "192.168.88.82", user = "root", psw = "12345678")
    ssh.execute_some_command('python3 /home/hpa/Desktop/ras_pi/script/link/link_drop_init.py')
    ssh.execute_some_command('exit')

def link_drop_read():
    ssh.login_host(host = "192.168.88.81", user = "root", psw = "12345678")
    ssh.execute_some_command('python3 /home/hpa/Desktop/ras_pi/script/link/link_drop_read.py')
    ssh.execute_some_command('exit')
    ssh.login_host(host = "192.168.88.82", user = "root", psw = "12345678")
    ssh.execute_some_command('python3 /home/hpa/Desktop/ras_pi/script/link/link_drop_read.py')
    ssh.execute_some_command('exit')
    
def SNR():
    ssh.login_host(host = "192.168.88.81", user = "root", psw = "12345678")
    ssh.execute_some_command('python3 /home/hpa/Desktop/ras_pi/script/SNR/SNR.py')
    ssh.execute_some_command('exit')
    ssh.login_host(host = "192.168.88.82", user = "root", psw = "12345678")
    ssh.execute_some_command('python3 /home/hpa/Desktop/ras_pi/script/SNR/SNR.py')
    ssh.execute_some_command('exit')
    
if __name__ == '__main__':
    eval(sys.argv[1] + '()')