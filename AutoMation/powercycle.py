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

globals.initialize()
config.IXIA_CONFIG()
config.POWERSWITCH_CONFIG()
config.CABLESWITCH_CONFIG()
config.nomal_variable()
config.default_register()

ssh = ShellHandler.ShellHandler()
telnet_client = telnet_powerswitch.TelnetClient()

for i in range(1,50):
    print("powercycle"+str(i)+" start")
    if telnet_client.login_host("192.168.88.66","teladmin","123456"):
        telnet_client.execute_some_command("sw o05 off imme")
        time.sleep(2)
        telnet_client.execute_some_command("sw o05 on imme")
        telnet_client.logout_host()
	
    ssh.login_host(host = "192.168.88.81", user = "root", psw = "12345678")
    user_dir = ssh.execute_some_command('/home/hpa/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/fapi-mdio-c45-write 99 28 0x1e 0xc 0x683')
    ssh.execute_some_command('exit')
    print("powercycle"+str(i)+" finish")
    time.sleep(10)