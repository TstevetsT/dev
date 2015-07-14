#! /usr/bin/env python
# This script is for parsing the output from an ns-3 simulation trace file and calculating 
# delivery ratio, dropped ratio, delay, hopct, and more.  the node number for source and sink
# USAGE
with open('siftTrace.tr') as f:
	lines =  f.read().splitlines() 
#Initialize Variables
sourcenode=99   # Eventually this will be a commandline set variable of node generating traffic
sinknode=0  # commandline set variable sink node number
txrx=0
time=1
node=2
seq=79
ttl=81
pric=[]
allcomms=[]
tx=[]
rx=[]
temp="  "
# For block will parse data to extract required data
for line in lines:  #range(0, len(lines)-1)
	pric.append(line.split(' ')[txrx])
        pric.append(float(line.split(' ')[time]))
        temp=line.split(' ')[node]
        pric.append(int(temp.split('/')[2]))
        pric.append(int(line.split(' ')[seq]))
        temp=line.split(' ')[ttl]
        pric.append(int(temp.split(')')[0]))
        allcomms.append(pric)
        if pric[txrx] == 't': 
		if int(pric[node]) == sourcenode:
			tx.append(pric)
        elif pric[txrx] == 'r': 
		if int(pric[node]) == sinknode:
                	rx.append(pric)
        pric=[]

seq=3
ttl=4
ntxpackets=len(tx)
nrxpackets=len(rx)
temprx=[]
temptx=[]
dropped=1
wttl=0
packetsdropped=0
packetsdelivered=0

#print(tx)
#print(rx)
j=0
i=0
for j in range(0, ntxpackets):
	for i in range(0, nrxpackets-1):
		#print "%d == %d" % (rx[i][seq], j+1)
		if rx[i][seq]==j+1:
			dropped=0
			temprx.append(rx[i])
			temptx.append(tx[j])
			packetsdelivered+=1
			break
j=0
delay=[]
hops=[]
for j in range(0, packetsdelivered):
	delay.append(temprx[j][time]-temptx[j][time])
	hops.append(temptx[j][ttl]-temprx[j][ttl])
print(delay)
print(hops)
averagedelay=sum(delay)/float(len(delay))
averagehops=sum(hops)/len(hops)
#print(averagedelay)
averagedelay=averagedelay*1000
	
packetsdropped=ntxpackets-packetsdelivered		
#print(temptx)
#print(temprx)
print("average hops/flow is " + str(averagehops) + " hops")
print("average delay/flow is " + str(averagedelay) +" milliseconds")
print("dropped " + str(packetsdropped) + " packet(s)")
print("delivered " + str(packetsdelivered) + " packet(s)")

