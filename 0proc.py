#! /usr/bin/env python
# This script is for parsing the output from an ns-3 simulation trace file and calculating 
# delivery ratio, dropped ratio, delay, hopct, and more.  the node number for source and sink
# USAGE  ./0proc.py <inputfilename>
# The nodes MUST be all have a unique last octet (Limited to 253 nodes)
# ToDo
# -  Make code work for all IP address (not dependent on unique last octet)
import sys
with open(sys.argv[1]) as f:
	lines =  f.read().splitlines() 
#Initialize Variables
#sourcenode=int(sys.argv[2])-1   
#sinknode=0  # commandline set variable sink node number
txrx=0
time=1
node=2
seq=79
ttl=81
srcip=54
dstip=70
pric=[]
allx=[]
tx=[]
rx=[]
temp="  "
# For block will parse data to extract required data fields
# Outputs:
# 	tx-a parsed list of all source transmitted traces
#       rx-a parsed list of all destination received traces
#       allx-a parsed list of all traces
# it will be in the following form:
# ['<txrx>', <time>, <processing node#>, <seq#>, <ttl>, <srclastoct>, <dstlastoct>] 
#      0       1              2             3      4           5            6
for line in lines:  #range(0, len(lines)-1)
	pric.append(line.split(' ')[txrx])
        pric.append(float(line.split(' ')[time]))
        temp=line.split(' ')[node]
        pric.append(int(temp.split('/')[2]))
        pric.append(int(line.split(' ')[seq]))
        temp=line.split(' ')[ttl]
        pric.append(int(temp.split(')')[0]))
        temp=line.split(' ')[srcip]
        pric.append((int(temp.split('.')[3])-1))
        temp=line.split(' ')[dstip]
        pric.append((int(temp.split('.')[3])-1))
        allx.append(pric)
        if pric[txrx] == 't':               # If packet is transmitted type and
		if pric[node] == pric[5]:   #    if processing node == source node
			tx.append(pric)     #    then save as source trace
        elif pric[txrx] == 'r': 	    # If trace type is recieved  AND
		if pric[node] == pric[6]:   # 	 if processing node == destination node
                	rx.append(pric)     # 	 then save as destination trace
        pric=[]

print(tx)
print(rx)
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
j=0
i=0
for j in range(0, ntxpackets):
	for i in range(0, nrxpackets):
		if rx[i][seq]==tx[j][seq]:
                	if rx[i][6]==tx[j][6]:
		                print "RxSeq=%d TxSeq=%d RxIP=%d TxIP=%d" %(rx[i][seq],tx[j][seq],rx[i][6],tx[j][6])
				dropped=0
				temprx.append(rx[i])
				temptx.append(tx[j])
				packetsdelivered+=1
				break
j=0
delay=[]
hops=[]
print(temptx)
print(temprx)
for j in range(0, packetsdelivered):
	delay.append(temprx[j][time]-temptx[j][time])
	hops.append(temptx[j][ttl]-temprx[j][ttl])
averagedelay=sum(delay)/float(len(delay))
averagehops=float(sum(hops))/float(len(hops))
averagedelay=averagedelay*1000   # Converts delay to milliseconds
packetsdropped=ntxpackets-packetsdelivered
pacdeliveryrate=float(packetsdelivered)/float(ntxpackets)
pacdroprate=1-pacdeliveryrate		
print("[Average hops/flow, Average delay (ms), # delivered, delivered rate, # dropped, dropped rate]")
output=[] 
output.append(averagehops)
output.append(averagedelay)
output.append(packetsdelivered)
output.append(pacdeliveryrate)
output.append(packetsdropped)
output.append(pacdroprate)
print(output)

