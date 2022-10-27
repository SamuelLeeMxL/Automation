import subprocess
import os
import sys
import datetime
import time

##### server=81 0x1c
##### execute pctool by subprocess 
##### stdin = write
##### stdout = read


#obj = subprocess.Popen(["./pctool", "0x1c"], cwd="/home/hpa/Desktop/ras_pi/mypg_ethswbox/ethswbox/build", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
obj = subprocess.Popen(["/home/hpa/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/pctool", sys.argv[1]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
##### write program
time.sleep(1)
obj.stdin.write("gpy2xx_init\n")
time.sleep(1)
obj.stdin.write("gpy2xx_soft_reset\n")
time.sleep(1)
obj.stdin.write("exit\n")
obj.stdin.close()
##### read program
cmd_out = obj.stdout.read()
obj.stdout.close()
### close subprocess
obj.terminate()
##### write to file
date_string = str(datetime.datetime.now())
print("**************************server=81 0x1c start")
print("Time is "+date_string)
print(cmd_out)