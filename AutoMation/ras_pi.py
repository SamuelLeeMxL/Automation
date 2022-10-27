import ShellHandler
import sys
import time
ssh = ShellHandler.ShellHandler()
import config
import datetime
import os.path

### args 1 : function name
### args 2 : port numbers
config.CABLESWITCH_CONFIG()
config.default_register()
ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
user_dir = ssh.execute_some_command('ls /home')
ssh.execute_some_command('exit')

def link_drop_init():
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/link/link_drop_init.py')
    ssh.execute_some_command('exit')
    

def link_drop_read():
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/link/link_drop_read.py')
    ssh.execute_some_command('exit')
    
def SNR():
    
    number = int(sys.argv[2])
    total_SNR = ""
    
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    i =0
    # ### phy address 0
    # SNR = ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/SNR/SNR.py 0')
    # time.sleep(5)
    # SNR_fix = SNR[2:-3]
    # total_SNR+=SNR_fix+","
    # ### phy address 5
    # SNR = ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/SNR/SNR.py 5')
    # time.sleep(5)
    # SNR_fix = SNR[2:-3]
    # total_SNR+=SNR_fix+","
    # ### phy address 3
    # SNR = ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/SNR/SNR.py 3')
    # time.sleep(5)
    # SNR_fix = SNR[2:-3]
    # total_SNR+=SNR_fix+","
    # ### phy address 5
    # SNR = ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/SNR/SNR.py 4')
    # time.sleep(5)
    # SNR_fix = SNR[2:-3]
    # total_SNR+=SNR_fix
    while i < number:
        n = int(config.device_address)+i
        SNR = ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/SNR/SNR.py '+str(n))
        #time.sleep(5)
        SNR_fix = SNR[2:-3]
        if (i==number-1):
            total_SNR+=SNR_fix
        else:
            total_SNR+=SNR_fix+","
        i=i+1
    ssh.execute_some_command('exit')
    print (total_SNR)
    return (total_SNR)
    

def SPEED_100M():
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    time.sleep(2) 
    ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/dd/mypg_ethswbox/ethswbox/build/fapi-gsw-mdio-write 28 0x9 0')
    time.sleep(2) 
    ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/dd/mypg_ethswbox/ethswbox/build/fapi-gsw-mdio-write 28 0x0 0x3240')
    time.sleep(2) 
    ssh.execute_some_command('exit')

def SPEED_1G():
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    time.sleep(2) 
    ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/dd/mypg_ethswbox/ethswbox/build/fapi-gsw-mdio-write 28 0x9 300')
    time.sleep(2) 
    ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/dd/mypg_ethswbox/ethswbox/build/fapi-gsw-mdio-write 28 0x0 0x3240')
    time.sleep(2) 
    ssh.execute_some_command('exit')  
    
def SWreset():
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    time.sleep(2) 
    ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/SWreset/SWreset.py 0')
    time.sleep(2) 
    ssh.execute_some_command('python3 /home/'+user_dir[2:-3]+'/Desktop/ras_pi/script/SWreset/SWreset.py 1')
    ssh.execute_some_command('exit')  

def MII_state():
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    time.sleep(1) 
    total_MII = ""
    # ### phy address 0
    # MII_log = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c45-read 99 0 0x0 0x18')
    # MII_start = MII_log.index('value=')+8
    # MII = MII_log[MII_start:-3]
    # total_MII+=str(MII)+","
    # ### phy address 5
    # MII_log = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c45-read 99 5 0x0 0x18')
    # MII_start = MII_log.index('value=')+8
    # MII = MII_log[MII_start:-3]
    # total_MII+=str(MII)+","
    # ### phy address 3
    # MII_log = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c45-read 99 3 0x0 0x18')
    # MII_start = MII_log.index('value=')+8
    # MII = MII_log[MII_start:-3]
    # total_MII+=str(MII)+","
    # ### phy address 4
    # MII_log = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c45-read 99 4 0x0 0x18')
    # MII_start = MII_log.index('value=')+8
    # MII = MII_log[MII_start:-3]
    # total_MII+=str(MII)    
    
    i = 28
    number = int(sys.argv[2]) 
    while i < number:
        n = int(config.device_address) + i
        MII_log = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c45-read 99 '+str(n)+' 0x0 0x18')
        MII_start = MII_log.index('value=')+8
        MII = MII_log[MII_start:-3]
        #print (str(n)+" "+str(MII))
        max_n = number-1
        if (i == max_n):
            total_MII+=str(MII)
        else:
            total_MII+=str(MII)+","
        #total_MII.append(str(MII)+",") 
        i=i+1
    ssh.execute_some_command('exit')  
    print (total_MII)
    return (total_MII)
  
def Link_up_time():
    start_time = time.time()
    phy_address = sys.argv[2]
    wait_time = sys.argv[3]
    print("phy_address"+phy_address)
    linkuptime = ""
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    #for i in range(1,30):
    j = 1
    for i in range(1,60):
        STD_STAT = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c45-read 99 '+phy_address+' 0x0 0x1')
        ### hawkville setting
        #STD_STAT = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/dd_pctool/dd/mypg_ethswbox/ethswbox/build/fapi-gsw-mdio-read '+phy_address+' 0x1')
        #if str(bin(int(STD_STAT[STD_STAT.index('val =')+8:-3], 16)))[-3] =="0":
        if str(bin(int(STD_STAT[STD_STAT.index('value=')+8:-3], 16)))[-3] =="0":
            if i == 60:
                print("link timeout")
            else:
                print("link down, wait moment")
            time.sleep(0.5)
        else:
            if j < 3:
               print(str(j)+" pass, check again...")
               j = j+1
               i = 1
            else :
                end_time = time.time()
                print("link up")
                linkuptime = str(round(end_time-start_time,3)+int(wait_time))
                #return (1)
                break;
    ssh.logout_host()
    #print("duration="+)
    if linkuptime != "":
        fp = open("duration.txt", "a")
        fp.write(phy_address+" "+linkuptime+" ")
        fp.close()
    return ("over")   
     
if __name__ == '__main__':
    eval(sys.argv[1] + '()')