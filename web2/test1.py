
#!/usr/bin/env python3


#import os
#import time

#import sys
 
# total arguments
#n = len(sys.argv)

#print("\nAPN Passed:", end = " ")

#s=""
#s=(sys.argv[1])

#print(s)

#s=s+'"'


#with open("/home/pi/apn.txt") as f:
#    lines = f.readlines() #read.
#modify.
#    lines[1] = 'connect "/usr/sbin/chat -v -f /etc/chatscripts/gprs -T ' +s+  '\n' #you can repla>

#with open("/home/pi/apn.txt", "w") as f:
#    f.writelines(lines) #write back.


#os.popen('sudo cp /home/pi/apn.txt /etc/ppp/peers/rnet')


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

#for i in range(1, n):
#    print(sys.argv[i], end = " ")
     
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
#s=s+"'"

#x= 'python /home/pi/2.py '+s
#print(x)

#os.popen('python /home/pi/2.py airtelgprs')

#time.sleep(1)
#exit

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

