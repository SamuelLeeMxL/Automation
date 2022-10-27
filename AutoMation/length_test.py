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

for i in range(0,60):
    ssh.login_host(host = "192.168.88.154", user = "root", psw = "arduino")
    ssh.execute_some_command('./blink.py 1')
    ssh.execute_some_command('exit')
    print ("length change to 200m")
    time.sleep(60)
    ssh.login_host(host = "192.168.88.154", user = "root", psw = "arduino")
    ssh.execute_some_command('./blink.py 8')
    ssh.execute_some_command('exit')
    print ("length change to 1m")
    time.sleep(10)