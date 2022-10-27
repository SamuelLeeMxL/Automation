def IXIA_CONFIG():
    global IXIA_IP
    IXIA_IP = "192.168.88.88"
    global MasterSlave
    MasterSlave = ['portMaster','portSlave']
    global Portspeeds
    Portspeeds = ['speed2500','speed1000']
    
def POWERSWITCH_CONFIG():
    global host_ip
    host_ip = '192.168.88.66'
    global username
    username = 'teladmin'
    global password
    password = '123456'
    global port
    port = '02'

def CABLESWITCH_CONFIG():
    global ArduinoIP
    ArduinoIP = ["192.168.88.103","192.168.88.104","192.168.88.153","192.168.88.154"]
    global RasPiIP
    RasPiIP = "192.168.88.82"
    global ArduinoSkip
    ArduinoSkip = "0000"
    global RasPiIPSkip
    RasPiIPSkip = "0"
    global CSports
    CSports = [1,8]
    global CSports_Forwarding
    CSports_Forwarding = [1,8]

def nomal_variable():
    global testtimes
    testtimes = 101
    global debug_flag
    debug_flag = 1

def default_register():
    global device_address
    device_address = "28"
    global register_short_name
    register_short_name = [["0x0", "STD_CTRL", "STD_STAT", "STD_PHYID1", "STD_PHYID2", "STD_AN_ADV", "STD_AN_LPA", "STD_AN_EXP", "STD_AN_NPTX", "STD_AN_NPRX", "STD_GCTRL", "STD_GSTAT", "STD_MMDCTRL", "STD_MMD_DATA", "STD_XSTAT", "PHY_STAT1", "PHY_CTL1", "PHY_CTL2", "PHY_ERRCNT", "PHY_MIISTAT", "PHY_IMASK", "PHY_ISTAT", "PHY_LED", "PHY_FWV"],
                           ["0x1", "PMA_CTRL1", "PMA_STAT1", "PMA_DEVID1", "PMA_DEVID2", "PMA_SPEED_ABILITY", "PMA_DIP1", "PMA_DIP2", "PMA_CTL2", "PMA_STAT2", "PMA_EXT_ABILITY", "PMA_PACKID1", "PMA_PACKID2", "PMA_MGBT_EXTAB", "PMA_MGBT_STAT", "PMA_MGBT_POLARITY", "PMA_MGBT_TX_PBO", "PMA_MGBT_TEST_MODE", "PMA_MGBT_SNR_OPMARGIN_A", "PMA_MGBT_SNR_OPMARGIN_B", "PMA_MGBT_SNR_OPMARGIN_C", "PMA_MGBT_SNR_OPMARGIN_D", "PMA_MGBT_MINMARGIN_A", "PMA_MGBT_MINMARGIN_B", "PMA_MGBT_MINMARGIN_C", "PMA_MGBT_MINMARGIN_D", "PMA_MGBT_POWER_A", "PMA_MGBT_POWER_B", "PMA_MGBT_POWER_C", "PMA_MGBT_POWER_D", "PMA_MGBT_SKEW_DELAY_0", "PMA_MGBT_SKEW_DELAY_1", "PMA_MGBT_FAST_RETRAIN_STA_CTRL", "PMA_TIMESYNC"],
                           ["0x3", "PCS_CTRL1", "PCS_STAT1", "PCS_DEVID1", "PCS_DEVID2", "PCS_SPEED_ABILITY", "PCS_DIP1", "PCS_DIP2", "PCS_CTRL2", "PCS_STAT2", "PCS_PACKID1", "PCS_PACKID2", "PCS_EEE_CAP", "PCS_EEE_CAP2", "PCS_EEE_WAKERR", "PCS_2G5_STAT1", "PCS_2G5_STAT2", "PCS_TIMESYNC_CAP"],
                           ["0x7", "ANEG_CTRL", "ANEG_STAT", "ANEG_DEVID1", "ANEG_DEVID2", "ANEG_DIP1", "ANEG_DIP2", "ANEG_PACKID1", "ANEG_PACKID2", "ANEG_ADV", "ANEG_LP_BP_AB", "ANEG_XNP_TX1", "ANEG_XNP_TX2", "ANEG_XNP_TX3", "ANEG_LP_XNP_AB1", "ANEG_LP_XNP_AB2", "ANEG_LP_XNP_AB3", "ANEG_MGBT_AN_CTRL", "ANEG_MGBT_AN_STA", "ANEG_EEE_AN_ADV1", "ANEG_EEE_AN_LPAB1", "ANEG_EEE_AN_ADV2", "ANEG_EEE_AN_LP_AB2", "ANEG_MGBT_AN_CTRL2"],
                           ["0x1e", "VSPEC1_LED0", "VSPEC1_LED1", "VSPEC1_LED2", "VSPEC1_SGMII_CTRL", "VSPEC1_SGMII_STAT", "VSPEC1_NBT_DS_CTRL", "VSPEC1_NBT_DS_STA", "VSPEC1_PM_CTRL", "VSPEC1_TEMP_STA", "VSPEC1_LANE_ASP_MAP"],
                           ["0x1f", "VPSPEC2_WOL_CTL", "VPSPEC2_WOL_AD01", "VPSPEC2_WOL_AD23", "VPSPEC2_WOL_AD45", "VPSPEC2_WOL_PW01", "VPSPEC2_WOL_PW23", "VPSPEC2_WOL_PW45"]
                          ]
    global register
    register = [["0x0", "0x0", "0x1", "0x2", "0x3", "0x4", "0x5", "0x6", "0x7", "0x8", "0x9", "0xa", "0xd", "0xe", "0xf", "0x11", "0x13", "0x14", "0x15","0x18", "0x19", "0x1a", "0x1b", "0x1e"],
                ["0x1", "0x0", "0x1", "0x2", "0x3", "0x4", "0x5", "0x6", "0x7", "0x8", "0xb", "0xe", "0xf", "0x15", "0x81", "0x82", "0x83", "0x84", "0x85", "0x86", "0x87", "0x88", "0x89", "0x8a", "0x8b", "0x8c", "0x8d", "0x8e", "0x8f", "0x90", "0x91", "0x92", "0x93", "0x708"],
                ["0x3", "0x0", "0x1", "0x2", "0x3", "0x4", "0x5", "0x6", "0x7", "0x8", "0xe", "0xf", "0x14", "0x15", "0x16", "0x20", "0x21", "0x708"],
                ["0x7", "0x0", "0x1", "0x2", "0x3", "0x5", "0x6", "0xe", "0xf", "0x10", "0x13", "0x16", "0x17", "0x18", "0x19", "0x1a", "0x1b", "0x20", "0x21", "0x3c", "0x3d", "0x3e", "0x3f", "0x40"],
                ["0x1e", "0x1", "0x2", "0x3", "0x8", "0x9", "0xa", "0xb", "0xc", "0xe", "0x14"],
                ["0x1f", "0xe06", "0xe08", "0xe09", "0xe0a", "0xe0b", "0xe0c", "0xe0d"]
               ]
    global default_register 
    default_register = [["0x0", "0x3040", "0x7949", "0x6749", "0xdc00", "0x0de1", "0x11w0", "0x0064", "0x2001", "0x0000", "0x200", "0x0", "0x0", "0x0", "0x2000", "0x0", "0x1", "0x6", "0x0", "0x0", "0x0", "0x0", "0xff00", "0x0"],
                        ["0x1", "0x2058", "0x0", "0x67c9", "0xdc00", "0x2070", "0x008b", "0xc000", "0x30", "0x8200", "0x41a0", "0x67c9", "0xdc00", "0x1", "0x0", "0x3", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0"],
                        ["0x3", "0x205c", "0x0", "0x67c9", "0xdc00", "0x40", "0x008b", "0xc000", "0xa", "0x9000", "0x67c9", "0xdc00", "0x6", "0x1", "0x0", "0x0", "0x0", "0x0"],
                        ["0x7", "0x3000", "0x8", "0x67c9", "0xdc00", "0x8b", "0xc000", "0x67c9", "0xdc00", "0x91e1", "0x1e0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0xa2", "0x0", "0x6", "0x0", "0x1", "0x1", "0x8"],
                        ["0x1e", "0x310", "0x320", "0x340", "0x30da", "0x8", "0x400", "0x0", "0x3", "0x0", "0xe4"],
                        ["0x1f", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0"]
                       ]
    
