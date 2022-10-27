import time
import globals
import config
import logging
import telnet_powerswitch
import os
import datetime
import ShellHandler
import tkinter as tk
from tkinter import messagebox as mb
import subprocess

################################################################################
# Globals value
################################################################################
globals.initialize()
config.IXIA_CONFIG()
config.POWERSWITCH_CONFIG()
config.CABLESWITCH_CONFIG()
config.nomal_variable()
config.default_register()
################################################################################
# Logging function
################################################################################
processurl = os.getcwd()
filename = input("Please enter filename:")
globals.str1 = filename
log_filename = datetime.datetime.now().strftime(filename + '_Main_%Y-%m-%d_%H_%M_%S.log')
if not os.path.exists('C:\\Python39\\Scripts\\Log'):
    os.makedirs('C:\\Python39\\Scripts\\Log')
os.mkdir('C:\\Python39\\Scripts\\Log\\'+log_filename, 777)
os.chdir('C:\\Python39\\Scripts\\Log\\'+log_filename)
logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                    datefmt = '%Y-%m-%d %H:%M:%S',
                    filename = log_filename)

formatter = logging.Formatter('%(asctime)s %(name)-8s %(levelname)-8s %(message)s')
logger = logging.getLogger('Main:')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)

################################################################################
# IXIA port
################################################################################
ssh = ShellHandler.ShellHandler()
IXIAport = input("Please enter IXIA setting port.(ex:5678):")
globals.str2 = IXIAport



if config.RasPiIPSkip=="0":
    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
    user_dir = ssh.execute_some_command('ls /home')
    print ("user="+user_dir[2:-3])
    # VERSION
    version_log = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c45-read 99 '+config.device_address+' 0x0 0x1e')
    ssh.execute_some_command('exit')
    version_start = version_log.index('value=')+6
    print ("version_log:"+str(version_log))
    print ("version_start:"+str(version_start))
    print (version_log[version_start:-3])
    f = open("version.txt", "a")
    f.write (version_log[version_start:-3])
    f.close()
else:
    version = input("Please enter version:")
    f = open("version.txt", "a")
    f.write (version)
    f.close()
    
################################################################################
# Start record time
################################################################################
time1 = time.localtime(time.time())
time_start = time1.tm_hour*3600 + time1.tm_min*60 + time1.tm_sec

################################################################################
# case start
################################################################################
print("Running case.\n\n Case 1 : Cable Plug in-out.\n Case 2 : Power on-off.\n Case 3 : Forwarding.\n Case 4 : HWreset.\n Case 5 : SWreset.\n Case 6 : Reang.\n Case 7 : Speed change.\n ")
print("If you want run case 1 case 2, please enter 11000 , 1 means run ,  0 means pass")
print("If you want run case 1 case 3, please enter 10100 , 1 means run ,  0 means pass")
print("If you want run case 4 case 5, please enter 00011 , 1 means run ,  0 means pass")
Running_case = input("Please enter Running case:")

################################################################################
# case 1 : Cable Plug in-out
################################################################################

if Running_case[0] == "0" :
    logger.info ('Case 1 Cable Plug : Ignore') 
   
if Running_case[0] == "1" :

    logger.info ('Case 1 Cable Plug : Start')
    
    for masterslave in config.MasterSlave :
        for csport in config.CSports :    
            for portspeed in config.Portspeeds :
                #print (portspeed)
                if portspeed == "speed100" and masterslave == "portSlave" :
                    logger.info (masterslave+" "+str(csport)+" "+portspeed+" igonre")
                    print (masterslave+" "+str(csport)+" "+portspeed)
                else :
                    i = 1
                    while i < config.testtimes :
                        fp = open("duration.txt","w")
                        fp.close()
                        a = 0
                        while a < len(globals.str2) :
                            if config.ArduinoSkip[a]=="0":
                                logger.info ('connect to '+config.ArduinoIP[a]+' ...')
                                ssh.login_host(host = config.ArduinoIP[a], user = "root", psw = "arduino")
                                ssh.execute_some_command('./blink.py 2')
                                logger.info ('Ethernet switch '+str(a)+' port change')
                                #time.sleep(2)
                                ssh.execute_some_command('./blink.py ' + str(csport) )
                                ssh.logout_host()
                                logger.info ('Ethernet switch '+str(a)+' port ' + str(csport) + ' on')
                                port_map = {"A": "10",
                                 "B": "11",
                                 "C": "12",
                                 "D": "13",
                                 "E": "14",
                                 "F": "15",
                                 "G": "16"}
                                subprocess.Popen(["tclsh", processurl+"\\ixia_api.tcl", port_map.get(globals.str2[a],globals.str2[a])])
                                #subprocess.Popen(["python", "C:\\python39\\Scripts\\Automation\\ras_pi.py", "Link_up_time", "28"])
                                ### havkville setting
                                #subprocess.Popen(["python", "C:\\python39\\Scripts\\Automation\\ras_pi.py", "Link_up_time", "5"])
                            else:
                                logger.info ('Ethernet switch '+str(a)+' skip')
                            print (csport)
                            a = a+1                            
                        j = 0
                        while j<30 :
                            fp = open("duration.txt","r")
                            duration_string = fp.read()
                            duration_split = duration_string.split(' ')
                            fp.close()
                            duration_index = len(duration_split)
                            if duration_index !=9:
                                time.sleep(1)
                            else:
                                break;
                            j = j+1
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150 "+config.RasPiIPSkip)
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")   
                        i=i+1
    logger.info ('Case 1 Cable Plug : End')
    
if Running_case[0] == "2" :

    logger.info ('Case 1-2 tenda case : Start')
    
    i = 1
    while i < config.testtimes :
        for masterslave in config.MasterSlave :
            for csport in config.CSports :    
                for portspeed in config.Portspeeds :
                #print (portspeed)
                    if config.ArduinoSkip[0]=="0":
                        ssh.login_host(host = config.ArduinoIP, user = "root", psw = "arduino")
                        ssh.execute_some_command('./blink.py 2')
                        ssh.logout_host()
                        logger.info ('Ethernet switch 1 port change')
                        ssh.login_host(host = config.ArduinoIP, user = "root", psw = "arduino")
                        ssh.execute_some_command('./blink.py ' + str(csport) )
                        ssh.logout_host()
                        logger.info ('Ethernet switch 1 port ' + str(csport) + ' on')
                    else:
                        logger.info ('Ethernet switch 1 skip')
                    if config.ArduinoSkip[1]=="0":
                        ssh.login_host(host = config.ArduinoIP2, user = "root", psw = "arduino")
                        ssh.execute_some_command('./blink.py 2')
                        ssh.logout_host()
                        logger.info ('Ethernet switch 2 port change')
                        ssh.login_host(host = config.ArduinoIP2, user = "root", psw = "arduino")                        
                        ssh.execute_some_command('./blink.py ' + str(csport) )
                        ssh.logout_host()
                        logger.info ('Ethernet switch 2 port ' + str(csport) + ' on')
                    else:
                        logger.info ('Ethernet switch 2 skip')
                    if config.ArduinoSkip[2]=="0":
                        ssh.login_host(host = config.ArduinoIP3, user = "root", psw = "arduino")
                        ssh.execute_some_command('./blink.py 2')
                        ssh.logout_host()
                        logger.info ('Ethernet switch 3 port change')
                        ssh.login_host(host = config.ArduinoIP3, user = "root", psw = "arduino")
                        ssh.execute_some_command('./blink.py ' + str(csport) )
                        ssh.logout_host()
                        logger.info ('Ethernet switch 3 port ' + str(csport) + ' on')
                    else:
                        logger.info ('Ethernet switch 3 skip')
                    if config.ArduinoSkip[3]=="0":    
                        ssh.login_host(host = config.ArduinoIP4, user = "root", psw = "arduino")
                        ssh.execute_some_command('./blink.py 2')
                        ssh.logout_host()
                        logger.info ('Ethernet switch 4 port change')
                        ssh.login_host(host = config.ArduinoIP4, user = "root", psw = "arduino")
                        ssh.execute_some_command('./blink.py ' + str(csport) )
                        ssh.logout_host()
                        logger.info ('Ethernet switch 4 port ' + str(csport) + ' on')
                    else:
                        logger.info ('Ethernet switch 4 skip')
                    print (csport)
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150 "+config.RasPiIPSkip)
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 portSlave "+str(csport)+" speed2500 "+str(i)+" 150 "+config.RasPiIPSkip)
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 portSlave "+str(csport)+" speed1000 "+str(i)+" 150 "+config.RasPiIPSkip)
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 portSlave "+str(csport)+" speed2500 "+str(i)+" 150 "+config.RasPiIPSkip)
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 portMaster "+str(csport)+" speed1000 "+str(i)+" 150 "+config.RasPiIPSkip)
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 portMaster "+str(csport)+" speed2500 "+str(i)+" 150 "+config.RasPiIPSkip)
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 portSlave "+str(csport)+" speed1000 "+str(i)+" 150 "+config.RasPiIPSkip)
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 portMaster "+str(csport)+" speed2500 "+str(i)+" 150 "+config.RasPiIPSkip)
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 3000 portMaster "+str(csport)+" speed1000 "+str(i)+" 150 "+config.RasPiIPSkip)
                        
                        
                        
                        
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")   
        i=i+1
    logger.info ('Case 1-2 tenda case : End')
    
if Running_case[0] == "3" :

    logger.info ('Case 1-3 switch loopback and nomal case : Start')
    
    i = 1
    while i < config.testtimes :
        for masterslave in config.MasterSlave :
            for csport in config.CSports :    
                for portspeed in config.Portspeeds :
                
                #print (portspeed)
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        
                        ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
                        ### write MII register 0.14 to 1 and check port 2 is loopback mode
                        logger.info ("write MII register 0.14 to 1")
                        ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 0 0x0 0x7040')
                        #time.sleep(0.1)
                        ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 0 0x0 0x3040')
                        #time.sleep(0.1)
                        ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 0 0x0 0x7040')
                        
                        # loopback_log = ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-read 99 0 0x0')
                        # loopback_log_start = loopback_log.index('value=')+6
                        # print ("loopback_log:"+str(loopback_log))
                        # print ("loopback_log_start:"+str(loopback_log_start))
                        # print (loopback_log[loopback_log_start:-3])
                        # fp = open("loopback_log.txt","a")
                        # fp.write("mode = "+masterslave+" "+"portspeed = "+portspeed+" "+str(i)+" MII 0.14 set 1  = "+loopback_log[loopback_log_start:-3]+"\n")
                        # fp.close()
                        fp = open("duration.txt","w")
                        fp.close()
                        subprocess.Popen(["python", "C:\\python39\\Scripts\\Automation\\ras_pi.py", "Link_up_time", "1"])
                        j = 0
                        while j<30 :
                            fp = open("duration.txt","r")
                            duration_string = fp.read()
                            duration_split = duration_string.split(' ')
                            fp.close()
                            duration_index = len(duration_split)
                            if duration_index !=3:
                                time.sleep(1)
                            else:
                                break;
                            j = j+1
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 2000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i+1)+" 150 "+config.RasPiIPSkip)
                        f = open("flag.txt", "r")
                        flag = int(f.read())
                        f.close()
                        if flag == 1:
                            print ("stop_y")
                            break  
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")   
                f = open("flag.txt", "r")
                flag = int(f.read())
                f.close()
                if flag == 1:
                    print ("stop_y")
                    break  
            f = open("flag.txt", "r")
            flag = int(f.read())
            f.close()
            if flag == 1:
                print ("stop_y")
                break  
        f = open("flag.txt", "r")
        flag = int(f.read())
        f.close()
        if flag == 1:
            print ("stop_y")
            break  
        i=i+1
    logger.info ('Case 1-3 switch loopback and nomal case : end')
    
################################################################################
# case 2 : Power Cycle
################################################################################

if Running_case[1] == "0" :
   logger.info ('Case 2 Power Cycle : Ignore') 

if Running_case[1] == "1" :
    logger.info ('Case 2 Power Cycle : Start')
    
    telnet_client = telnet_powerswitch.TelnetClient()
    command = 'sw o'+config.port+' on imme'
    if telnet_client.login_host(config.host_ip,config.username,config.password):
       telnet_client.execute_some_command(command)
       telnet_client.logout_host()

    for masterslave in config.MasterSlave :
        for csport in config.CSports :
            fp = open("duration.txt","w")
            fp.close()
            a = 0
            while a < len(globals.str2) :
                if config.ArduinoSkip[a]=="0":
                    logger.info ('connect to '+config.ArduinoIP[a]+' ...')
                    ssh.login_host(host = config.ArduinoIP[a], user = "root", psw = "arduino")
                    ssh.execute_some_command('./blink.py ' + str(csport) )
                    ssh.logout_host()
                    logger.info ('Ethernet switch '+str(a)+' port ' + str(csport) + ' on')
                else :
                    logger.info ('Ethernet switch '+str(a)+' skip')
                print (csport)
                a = a+1      
                
            for portspeed in config.Portspeeds :
                    ## start traffic step                    
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed)
                    else :
                        i = 1
                        while i < config.testtimes :
                            ### power off step
                            logger.info ('power off')
                            command = 'sw o'+config.port+' off imme'       
                            if telnet_client.login_host(config.host_ip,config.username,config.password):
                                telnet_client.execute_some_command(command)
                                telnet_client.logout_host()
                            time.sleep(5)
                            ### power on step
                            logger.info ('power on')
                            command = 'sw o'+config.port+' on imme'       
                            if telnet_client.login_host(config.host_ip,config.username,config.password):
                                telnet_client.execute_some_command(command)
                                telnet_client.logout_host()
                            a = 0
                            while a < len(globals.str2) :
                                port_map = {"A": "10",
                                 "B": "11",
                                 "C": "12",
                                 "D": "13",
                                 "E": "14",
                                 "F": "15",
                                 "G": "16"}
                                subprocess.Popen(["tclsh", processurl+"\\ixia_api.tcl", port_map.get(globals.str2[a],globals.str2[a])])
                                a = a+1
                            j = 0
                            while j<30 :
                                fp = open("duration.txt","r")
                                duration_string = fp.read()
                                duration_split = duration_string.split(' ')
                                fp.close()
                                duration_index = len(duration_split)
                                if duration_index !=9:
                                    time.sleep(1)
                                else:
                                    break;
                                j = j+1
                            logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                            print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                            os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" powercycle 1518 5 3000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150 "+config.RasPiIPSkip)
                            logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")
                            i=i+1
    logger.info ('Case 2 Power Cycle : End')

################################################################################
# case 3 : Forwarding
# 0: Ignore 
# 1: run forwarding case
# 2: run forwarding bundle case
################################################################################
if Running_case[2] == "0" :
    logger.info ('Case 3 Forwarding : Ignore')

if Running_case[2] == "1" :

    logger.info ('Case 3 Forwarding : Start')
    for masterslave in config.MasterSlave :
        for csport in config.CSports_Forwarding :
            fp = open("duration.txt","w")
            fp.close()
            a = 0
            while a < len(globals.str2) :
                if config.ArduinoSkip[a]=="0":
                    logger.info ('connect to '+config.ArduinoIP[a]+' ...')
                    ssh.login_host(host = config.ArduinoIP[a], user = "root", psw = "arduino")
                    ssh.execute_some_command('./blink.py ' + str(csport) )
                    ssh.logout_host()
                    logger.info ('Ethernet switch '+str(a)+' port ' + str(csport) + ' on')
                    port_map = {"A": "10",
                                "B": "11",
                                "C": "12",
                                "D": "13",
                                "E": "14",
                                "F": "15",
                                "G": "16"}
                    subprocess.Popen(["tclsh", processurl+"\\ixia_api.tcl", port_map.get(globals.str2[a],globals.str2[a])])
                else :
                    logger.info ('Ethernet switch '+str(a)+' skip')
                print (csport)
                a = a+1
            j = 0
            while j<30 :
                fp = open("duration.txt","r")
                duration_string = fp.read()
                duration_split = duration_string.split(' ')
                fp.close()
                duration_index = len(duration_split)
                if duration_index !=9:
                    time.sleep(1)
                else:
                    break;
                j = j+1
            for portspeed in config.Portspeeds :
                i = 1
                if portspeed == "speed100" and masterslave == "portSlave" :
                    logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                    print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                else :
                    logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                    print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding 64 5 3600000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50 "+config.RasPiIPSkip)
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding 1518 5 3600000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50 "+config.RasPiIPSkip)
                    os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding random 4 3600000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50 "+config.RasPiIPSkip)
                    # f = open("flag.txt", "r")
                    # flag = int(f.read())
                    # f.close()
                    # if flag == 1:
                        # print ("stop_y")
                        # break  
                logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")
                        
            # f = open("flag.txt", "r")
            # flag = int(f.read())
            # f.close()
            # if flag == 1:
                # print ("stop_y")
                # break  

        # f = open("flag.txt", "r")
        # flag = int(f.read())
        # f.close()
        # if flag == 1:
            # print ("stop_y")
            # break  

    logger.info ('Case 3 Forwarding : End')
    
if Running_case[2] == "2" :

    logger.info ('Case 3 Bundle test : Start')
    for masterslave in config.MasterSlave :
        for csport in config.CSports_Forwarding :
            print (csport)
            for portspeed in config.Portspeeds :
                i = 1
                while i < config.testtimes :
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" bundle 1518 4 3600000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50 "+config.RasPiIPSkip)
                    i=i+1
                logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")

    logger.info ('Case 3 Bundle test : End')
    
if Running_case[2] == "3" :

    logger.info ('Case 3 Endurance test : Start')
    for masterslave in config.MasterSlave :
        for csport in config.CSports_Forwarding :
            print (csport)
            for portspeed in config.Portspeeds :
                i = 1
                while i < config.testtimes :
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" endurance 1518 4 259200000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50 "+config.RasPiIPSkip)
                    i=i+1
                logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")

    logger.info ('Case 3 Endurance test : End')


################################################################################
# case 4 : HWreset
################################################################################

if Running_case[3] == "0" :
   logger.info ('Case 4 HWreset : Ignore') 

if Running_case[3] == "1" :
    logger.info ('Case 4 HWreset : Start')
    
    for masterslave in config.MasterSlave :
        for csport in config.CSports :
            fp = open("duration.txt","w")
            fp.close()
            a = 0
            while a < len(globals.str2) :
                if config.ArduinoSkip[a]=="0":
                    logger.info ('connect to '+config.ArduinoIP[a]+' ...')
                    ssh.login_host(host = config.ArduinoIP[a], user = "root", psw = "arduino")
                    ssh.execute_some_command('./blink.py ' + str(csport) )
                    ssh.logout_host()
                    logger.info ('Ethernet switch '+str(a)+' port ' + str(csport) + ' on')
                else :
                    logger.info ('Ethernet switch '+str(a)+' skip')
                print (csport)
                a = a+1
            for portspeed in config.Portspeeds :
                i = 1
                while i < config.testtimes :
                    logger.info ('Device reset start')
                    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
                    ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/gpio22_rst')
                    ssh.execute_some_command('exit')
                    logger.info ('device reset finish')
                    a = 0
                    while a < len(globals.str2) :
                        port_map = {"A": "10",
                        "B": "11",
                        "C": "12",
                        "D": "13",
                        "E": "14",
                        "F": "15",
                        "G": "16"}
                        subprocess.Popen(["tclsh", processurl+"\\ixia_api.tcl", port_map.get(globals.str2[a],globals.str2[a])])
                        a = a+1
                    j = 0
                    while j<30 :
                        fp = open("duration.txt","r")
                        duration_string = fp.read()
                        duration_split = duration_string.split(' ')
                        fp.close()
                        duration_index = len(duration_split)
                        if duration_index !=9:
                            time.sleep(1)
                        else:
                            break;
                        j = j+1
                    
                    ### start traffic step                    
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" HWreset 1518 5 3000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150 "+config.RasPiIPSkip)
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")
                    i=i+1
    logger.info ('Case 4 Reset : End')
    
################################################################################
# case 5 : SWreset
################################################################################

if Running_case[4] == "0" :
   logger.info ('Case 5 SWreset : Ignore') 

if Running_case[4] == "1" :
    logger.info ('Case 5 SWreset : Start')
    
    for masterslave in config.MasterSlave :
        for csport in config.CSports :
            a = 0
            while a < len(globals.str2) :
                if config.ArduinoSkip[a]=="0":
                    logger.info ('connect to '+config.ArduinoIP[a]+' ...')
                    ssh.login_host(host = config.ArduinoIP[a], user = "root", psw = "arduino")
                    ssh.execute_some_command('./blink.py ' + str(csport) )
                    ssh.logout_host()
                    logger.info ('Ethernet switch '+str(a)+' port ' + str(csport) + ' on')
                else :
                    logger.info ('Ethernet switch '+str(a)+' skip')
                print (csport)
                a = a+1
            for portspeed in config.Portspeeds :
                 
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed)
                    # elif portspeed == "speed1000" and masterslave == "portSlave" and str(csport)=="1" :
                        # logger.info (masterslave+" "+str(csport)+" "+portspeed+" igonre, known issue(long linkup time)")
                        # print (masterslave+" "+str(csport)+" "+portspeed)
                    else :
                        i = 1
                        fp = open("duration.txt","w")
                        fp.close()
                        while i < config.testtimes :
                            logger.info ('Device SWreset start')
                            ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
                            ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 '+config.device_address+' 0x0 0xb040')
                            ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 '+str(int(config.device_address)+1)+' 0x0 0xb040')
                            ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 '+str(int(config.device_address)+2)+' 0x0 0xb040')
                            ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 '+str(int(config.device_address)+3)+' 0x0 0xb040')
                            ssh.execute_some_command('exit')
                            a = 0
                            while a < len(globals.str2) :
                                port_map = {"A": "10",
                                            "B": "11",
                                            "C": "12",
                                            "D": "13",
                                            "E": "14",
                                            "F": "15",
                                            "G": "16"}
                                subprocess.Popen(["tclsh", processurl+"\\ixia_api.tcl", port_map.get(globals.str2[a],globals.str2[a])])
                                a = a+1
                            j = 0
                            while j<30 :
                                fp = open("duration.txt","r")
                                duration_string = fp.read()
                                duration_split = duration_string.split(' ')
                                fp.close()
                                duration_index = len(duration_split)
                                if duration_index !=9:
                                    time.sleep(1)
                                else:
                                    break;
                                j = j+1
                            ssh.execute_some_command('exit')
                            logger.info ('device SWreset finish') 
                            logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                            print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                            os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" SWreset 1518 5 3000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150 "+config.RasPiIPSkip)
                            logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")
                            i=i+1
    logger.info ('Case 5 SWreset : End')
    
################################################################################
# case 6 : Reang
################################################################################

if Running_case[5] == "0" :
   logger.info ('Case 6 Reang : Ignore') 

if Running_case[5] == "1" :
    logger.info ('Case 6 Reang : Start')    
    for masterslave in config.MasterSlave :
        for csport in config.CSports :
            a = 0
            while a < len(globals.str2) :
                if config.ArduinoSkip[a]=="0":
                    logger.info ('connect to '+config.ArduinoIP[a]+' ...')
                    ssh.login_host(host = config.ArduinoIP[a], user = "root", psw = "arduino")
                    ssh.execute_some_command('./blink.py ' + str(csport) )
                    ssh.logout_host()
                    logger.info ('Ethernet switch '+str(a)+' port ' + str(csport) + ' on')
                else :
                    logger.info ('Ethernet switch '+str(a)+' skip')
                print (csport)
                a = a+1
            for portspeed in config.Portspeeds :
                
                    
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    # elif portspeed == "speed1000" and masterslave == "portSlave" and str(csport)=="1" :
                        # logger.info (masterslave+" "+str(csport)+" "+portspeed+" igonre, known issue(long linkup time)")
                        # print (masterslave+" "+str(csport)+" "+portspeed)
                    else :
                        i = 1
                        while i < config.testtimes :
                            logger.info ('Device Reang start')      
                            ### reang start
                            fp = open("duration.txt","w")
                            fp.close()
                            ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
                            ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 28 0x0 0x3240')
                            logger.info ('Reang port 1') 
                            ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 29 0x0 0x3240')
                            logger.info ('Reang port 2') 
                            ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 30 0x0 0x3240')
                            logger.info ('Reang port 3') 
                            ssh.execute_some_command('/home/'+user_dir[2:-3]+'/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c22-write 99 31 0x0 0x3240')
                            logger.info ('Reang port 4') 
                            ssh.execute_some_command('exit')
                            a = 0
                            while a < len(globals.str2) :
                                port_map = {"A": "10",
                                 "B": "11",
                                 "C": "12",
                                 "D": "13",
                                 "E": "14",
                                 "F": "15",
                                 "G": "16"}
                                subprocess.Popen(["tclsh", processurl+"\\ixia_api.tcl", port_map.get(globals.str2[a],globals.str2[a])])
                                a = a+1
                            j = 0
                            while j<30 :
                                fp = open("duration.txt","r")
                                duration_string = fp.read()
                                duration_split = duration_string.split(' ')
                                fp.close()
                                duration_index = len(duration_split)
                                if duration_index !=9:
                                    time.sleep(1)
                                else:
                                    break;
                                j = j+1
                            logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                            print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                            os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" reang 1518 5 3000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150 "+config.RasPiIPSkip)
                            logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")
                            i=i+1
    logger.info ('Case 6 Reang : End')
    
################################################################################
# case 7 : Speed change
################################################################################
    
if Running_case[6] == "0" :
    logger.info ('Case 7 Speed change : Ignore') 
   
if Running_case[6] == "1" :

    logger.info ('Case 7 Speed change : Start')
    
    for masterslave in config.MasterSlave :
        for csport in config.CSports :
            print (csport)
            ssh.login_host(host = config.ArduinoIP, user = "root", psw = "arduino")
            ssh.execute_some_command('./blink.py ' + str(csport) )
            ssh.execute_some_command('exit')
            logger.info ('Ethernet switch1 port ' + str(csport) + ' on')
            time.sleep(5) 
            ssh.login_host(host = config.ArduinoIP2, user = "root", psw = "arduino")
            ssh.execute_some_command('./blink.py ' + str(csport) )
            ssh.execute_some_command('exit')
            logger.info ('Ethernet switch2 port ' + str(csport) + ' on')
            time.sleep(5) 
            ssh.login_host(host = config.ArduinoIP3, user = "root", psw = "arduino")
            ssh.execute_some_command('./blink.py ' + str(csport) )
            ssh.execute_some_command('exit')
            logger.info ('Ethernet switch3 port ' + str(csport) + ' on')
            time.sleep(5) 
            ssh.login_host(host = config.ArduinoIP4, user = "root", psw = "arduino")
            ssh.execute_some_command('./blink.py ' + str(csport) )
            ssh.execute_some_command('exit')
            logger.info ('Ethernet switch4 port ' + str(csport) + ' on')
            time.sleep(30) 
            i = 1
            while i < config.testtimes :                
                for portspeed in config.Portspeeds :
                    print (portspeed)
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" speedchange 1518 5 10000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150 "+config.RasPiIPSkip)
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")   
                i=i+1
        logger.info ('Case 7 Speed change : End')