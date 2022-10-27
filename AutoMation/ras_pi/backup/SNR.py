import subprocess
import os
import sys
import datetime

##### server=81 0x1c
##### execute pctool by subprocess 
##### stdin = write
##### stdout = read
SNR_total =""
obj = subprocess.Popen(["/home/hpa/Desktop/ras_pi/mypg_ethswbox/ethswbox/build/pctool", sys.argv[1]], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

##### write program
obj.stdin.write("gpy2xx_init\n")
obj.stdin.write("gpy2xx_get_phy_id\n")

### get p0 SNR
obj.stdin.write("gpy2xx_read_mmd devtype=0x01 regaddr=133\n")
obj.stdin.write("\n")
obj.stdin.write("gpy2xx_read_mmd devtype=0x01 regaddr=134\n")
obj.stdin.write("\n")
obj.stdin.write("gpy2xx_read_mmd devtype=0x01 regaddr=135\n")
obj.stdin.write("\n")
obj.stdin.write("gpy2xx_read_mmd devtype=0x01 regaddr=136\n")
obj.stdin.write("\n")
obj.stdin.write("exit\n")
obj.stdin.close()
##### read program
cmd_out = obj.stdout.read()
obj.stdout.close()
### close subprocess
obj.terminate()
##### write to file
### regaddr=133
for i in range(3,7):
    find_string_start = cmd_out.find('regaddr=13'+str(i))
    find_string_end = cmd_out[find_string_start:].find('Shell :')+find_string_start
    SNR_value = cmd_out[find_string_start+27:find_string_end-3]
    if (i==6):
        SNR_total+= str(SNR_value)
    else:
        SNR_total+= str(SNR_value)+"-"
    
print(SNR_total)