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


################################################################################
# Globals value
################################################################################
globals.initialize()
config.IXIA_CONFIG()
config.POWERSWITCH_CONFIG()
config.CABLESWITCH_CONFIG()
config.nomal_variable()
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
IXIAport = input("Please enter IXIA setting port.(ex:5678):")
globals.str2 = IXIAport
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
# All Config
################################################################################
ssh = ShellHandler.ShellHandler()

### IXIA part
#IXIA_IP = config.IXIA_IP
#MasterSlave = config.MasterSlave
#Portspeeds = config.Portspeeds      #Single rate ['speed1000']         #Two test rate ['speed2.5g','speed1000']
#frameRate_rate = config.frameRate_rate
#frameRate_rate2 = 99

### Cable Switch Part
#ArduinoIP = "192.168.88.79"
#CSports = [1,2,3,4,5,6,7,8]                   ## 1=80m , 8=1m

### others
#testtimes = 101

################################################################################
# case start
################################################################################
print("Running case.\n\n Case 1 : Cable Plug in-out.\n Case 2 : Power on-off.\n Case 3 : Forwarding.\n Case 4 : Reset.\n")
print("If you want run case 1 case 2, please enter 110 , 1 means run ,  0 means pass")
print("If you want run case 1 case 3, please enter 101 , 1 means run ,  0 means pass\n")
Running_case = input("Please enter Running case:")
print(Running_case[0])
print(Running_case[1])
print(Running_case[2])

################################################################################
# case 1 : Cable Plug in-out
################################################################################

if Running_case[0] == "0" :
    logger.info ('Case 1 Cable Plug : Ignore') 
   
if Running_case[0] == "1" :

    logger.info ('Case 1 Cable Plug : Start')
    #### CablePlug case
    #### function.tcl
    #### option 0 : IXIA address
    #### option 1 : IXIA port1
    #### option 2 : IXIA port2
    #### option 3 : mode
    #### option 4 : masterslave
    #### option 5 : CSports
    #### option 6 : portspeed
    # #### option 7 : numbers
    # ssh.login_host(host = "192.168.88.81", user = "root", psw = "12345678")
    # ssh.execute_some_command('rm *.txt')
    # ssh.execute_some_command('exit')
    # ssh.login_host(host = "192.168.88.82", user = "root", psw = "12345678")
    # ssh.execute_some_command('rm *.txt')
    # ssh.execute_some_command('exit')
    for masterslave in config.MasterSlave :
    #print (masterslave)
        for csport in config.CSports :
            #print (csport)
            # ssh.login_host(host = config.ArduinoIP, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch1 port ' + str(csport) + ' on')
            # time.sleep(5) 
            # ssh.login_host(host = config.ArduinoIP2, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch2 port ' + str(csport) + ' on')
            # time.sleep(5) 
            # ssh.login_host(host = config.ArduinoIP3, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch3 port ' + str(csport) + ' on')
            # time.sleep(5) 
            # ssh.login_host(host = config.ArduinoIP4, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch4 port ' + str(csport) + ' on')
            # time.sleep(10) 
            ### it is support 2 port cable swtich
            for portspeed in config.Portspeeds :
                #print (portspeed)
                i = 1
                while i < config.testtimes :
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" cableplug 1518 5 10000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150")
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")
                    i=i+1
    logger.info ('Case 1 Cable Plug : End')
    
################################################################################
# case 2 : Power Cycle
################################################################################

if Running_case[1] == "0" :
   logger.info ('Case 2 Power Cycle : Ignore') 

if Running_case[1] == "1" :
    logger.info ('Case 2 Power Cycle : Start')
    #### Power on-off case
    #### function.tcl
    #### option 0 : IXIA address
    #### option 1 : IXIA port1
    #### option 2 : IXIA port2
    #### option 3 : mode
    #### option 4 : masterslave
    #### option 5 : CSports
    #### option 6 : portspeed
    #### option 7 : numbers
    # # CSports = [8]
    # ssh.login_host(host = "192.168.88.81", user = "root", psw = "12345678")
    # ssh.execute_some_command('rm *.txt')
    # ssh.execute_some_command('exit')
    # ssh.login_host(host = "192.168.88.82", user = "root", psw = "12345678")
    # ssh.execute_some_command('rm *.txt')
    # ssh.execute_some_command('exit')
    
    telnet_client = telnet_powerswitch.TelnetClient()
    command = 'sw o'+config.port+' on imme'
    if telnet_client.login_host(config.host_ip,config.username,config.password):
       telnet_client.execute_some_command(command)
       telnet_client.logout_host()

    for masterslave in config.MasterSlave :
        for csport in config.CSports :
            # print (csport)
            # ssh.login_host(host = config.ArduinoIP, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch 1 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP2, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch 2 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP3, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch 3 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP4, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch 4 port ' + str(csport) + ' on')
            # time.sleep(10)
            for portspeed in config.Portspeeds :
                #print (portspeed)
                i = 1
                while i < config.testtimes :
                    ### power off step
                    # logger.info ('power off')
                    # command = 'sw o'+config.port+' off imme'       
                    # if telnet_client.login_host(config.host_ip,config.username,config.password):
                        # telnet_client.execute_some_command(command)
                        # telnet_client.logout_host()
                    # time.sleep(10)
                    # ### power on step
                    # logger.info ('power on')
                    # command = 'sw o'+config.port+' on imme'       
                    # if telnet_client.login_host(config.host_ip,config.username,config.password):
                        # telnet_client.execute_some_command(command)
                        # telnet_client.logout_host()
                    # time.sleep(10)
                    ### start traffic step                    
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" powercycle 1518 5 10000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 150")
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
    # ssh.login_host(host = "192.168.88.81", user = "root", psw = "12345678")
    # ssh.execute_some_command('rm *.txt')
    # ssh.execute_some_command('exit')
    # ssh.login_host(host = "192.168.88.82", user = "root", psw = "12345678")
    # ssh.execute_some_command('rm *.txt')
    # ssh.execute_some_command('exit')
    logger.info ('Case 3 Forwarding : Start')
    # #### forwarding case
    # #### function.tcl
    # #### option 0 : IXIA address
    # #### option 1 : IXIA port1
    # #### option 2 : IXIA port2
    # #### option 3 : mode
    # #### option 4 : masterslave
    # #### option 5 : CSports
    # #### option 6 : portspeed
    # #### option 7 : numbers
    for masterslave in config.MasterSlave :
    #print (masterslave)
        for csport in config.CSports_Forwarding :
            # print (csport)
            # ssh.login_host(host = config.ArduinoIP, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch1 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP2, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch2 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP3, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch3 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP4, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch4 port ' + str(csport) + ' on')
            # time.sleep(10)
            for portspeed in config.Portspeeds :
                #print (portspeed)
                i = 1
                
                if portspeed == "speed100" and masterslave == "portSlave" :
                    logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                    print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                else :
                    logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                    print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    
                    ### forwarding 64byte 5min
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding 64 5 300000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50")
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding 64 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    ### flag function, value=1 it will stop
                    # f = open("flag.txt", "r")
                    # flag = int(f.read())
                    # f.close()
                    # if flag == 1:
                        # print ("stop_y")
                        # break  
                
                    # ### forwarding 1518byte 5min  
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding 1518 5 300000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50")
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding 1518 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    ### flag function, value=1 it will stop
                    # f = open("flag.txt", "r")                                                                                                                                                                                                       
                    # flag = int(f.read())
                    # f.close()
                    # if flag == 1:
                        # print ("stop_y")
                        # break 
                    
                    ### forwarding random 5min
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding random 5 300000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50")
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding random "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    # f = open("flag.txt", "r")
                    # flag = int(f.read())
                    # f.close()
                    # if flag == 1:
                        # print ("stop_y")
                        # break 
                
                    ### forwarding 1518 1hour
                    os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding 1518 4 3600000 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+" 50")
                    #os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" forwarding hour "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
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






################################################################################
# case 4 : Reset
################################################################################

if Running_case[3] == "0" :
   logger.info ('Case 4 Reset : Ignore') 

if Running_case[3] == "1" :
    logger.info ('Case 4 Reset : Start')
    #### Reset case
    #### function.tcl
    #### option 0 : IXIA address
    #### option 1 : IXIA port1
    #### option 2 : IXIA port2
    #### option 3 : mode
    #### option 4 : masterslave
    #### option 5 : CSports
    #### option 6 : portspeed
    #### option 7 : numbers
    # CSports = [8]
    
    for masterslave in config.MasterSlave :
        for csport in config.CSports :
            print (csport)
            # ssh.login_host(host = config.ArduinoIP, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch 1 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP2, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch 2 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP3, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch 3 port ' + str(csport) + ' on')
            # time.sleep(5)
            # ssh.login_host(host = config.ArduinoIP4, user = "root", psw = "arduino")
            # ssh.execute_some_command('./blink.py ' + str(csport) )
            # ssh.execute_some_command('exit')
            # logger.info ('Ethernet switch 4 port ' + str(csport) + ' on')
            # time.sleep(10)
            for portspeed in config.Portspeeds :
                #print (portspeed)
                i = 1
                while i < config.testtimes :
                    ### power off step
                    logger.info ('Device reset start')
                    ssh.login_host(host = config.RasPiIP, user = "root", psw = "12345678")
                    ssh.execute_some_command('/home/hpa/Desktop/mypg_ethswbox/ethswbox/build/gpio22_rst')
                    time.sleep(10)
                    ssh.execute_some_command('exit')
                    logger.info ('device reset finish')
                    ### start traffic step                    
                    if portspeed == "speed100" and masterslave == "portSlave" :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " igonre")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                    else :
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i)+ " start!")
                        print (masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        os.system("tclsh "+processurl+"\\function.tcl "+config.IXIA_IP+" "+globals.str2+" reset 1518 "+masterslave+" "+str(csport)+" "+portspeed+" "+str(i))
                        logger.info (masterslave+" "+str(csport)+" "+portspeed+" "+str(i) + " end!")
                    i=i+1
    logger.info ('Case 4 Reset : End')