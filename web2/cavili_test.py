
#!/usr/bin/env python3


import sys
import os
import subprocess
 

n = len(sys.argv)

print("\nAPN Passed:", end = " ")

Sum = 0

s=""
s=(sys.argv[1])

print(s)


s='"'+s+'"'
print(s)
#command ='atcom --port /dev/ttyACM0 AT+CGDCONT?'
#os.popen('atcom --port /dev/ttyACM0 AT+CGDCONT=1,"IP","airtelgprs.com"')
command='atcom --port /dev/ttyACM0 AT+CGDCONT=1,"IP",' + s
try:  
    output = subprocess.check_output(command, shell=True)
    output= ((output).decode('ascii'))
                           

except subprocess.CalledProcessError as e:
                
    output=(e.output)
            
print(output)

