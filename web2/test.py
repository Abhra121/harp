
#!/usr/bin/env python3


import os


import sys
 
# total arguments
n = len(sys.argv)

print("\nAPN Passed:", end = " ")

s=""
s=(sys.argv[1])
s=s+'"'


with open("/home/pi/apn.txt") as f:
    lines = f.readlines() #read.
#modify.
    lines[1] = 'connect "/usr/sbin/chat -v -f /etc/chatscripts/gprs -T ' +s+  '\n' #you can repla>

with open("/home/pi/apn.txt", "w") as f:
    f.writelines(lines) #write back.


os.popen('sudo cp /home/pi/apn.txt /etc/ppp/peers/rnet')



