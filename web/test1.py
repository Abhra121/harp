
#!/usr/bin/env python3


import sys
import os
import subprocess
 
# total arguments
n = len(sys.argv)
#print("Total arguments passed:", n)
 
# Arguments passed
#print("\nName of Python script:", sys.argv[0])
 
print("\nAPN Passed:", end = " ")
#print("APN is:\n")

# Addition of numbers
Sum = 0
# Using argparse module
#for i in range(1, n):
#    Sum += int(sys.argv[i])
     
#print("\n\nResult:", Sum)
#print(sys.argv[1])
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

