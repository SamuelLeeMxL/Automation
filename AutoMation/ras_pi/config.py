def IXIA_CONFIG():
    global IXIA_IP
    IXIA_IP = "192.168.88.88"
    global MasterSlave
    #MasterSlave = ['portSlave']
    MasterSlave = ['portMaster','portSlave']
    global Portspeeds
    Portspeeds = ['speed2500']
    #Portspeeds = ['speed1000','speed100']
    
def POWERSWITCH_CONFIG():
    global host_ip
    host_ip = '192.168.88.55'
    global username
    username = 'teladmin'
    global password
    password = '123456'
    global port
    port = '08'

def CABLESWITCH_CONFIG():
    global ArduinoIP
    ArduinoIP = "192.168.88.77"
    global ArduinoIP2
    ArduinoIP2 = "192.168.88.78"
    global ArduinoIP3
    ArduinoIP3 = "192.168.88.79"
    global ArduinoIP4
    ArduinoIP4 = "192.168.88.80"
    global RasPiIP
    RasPiIP = "192.168.88.81"
    global CSports
    CSports = [1]
    global CSports_Forwarding
    ### it is interation 
    CSports_Forwarding = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    #CSports_Forwarding = [8]

def ras_pi():
    global ras_pi_1    
def nomal_variable():
    global testtimes
    testtimes = 51
    global debug_flag
    debug_flag = 1