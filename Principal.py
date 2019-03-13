#!/usr/bin/python3
from socket import *
import requests
from Operator import *
import icmp_checksum3
import time
import os
import struct
import threading
import socketserver
import urllib.request

def start():
	res0 = S0();
	printarch("Step0",res0);
	fcode0 = makecode(res0,5,True);
	res1 = S1(fcode0);
	printarch("Step1",res1);
	fcode1 = makecode(res1,4,False);
	res2 = S2p1(fcode1);
	printarch("Step2",res2);
	fcode2 = makecode(res2,5,False);
	res3 = S3(fcode2);
	printarch("Step3",res3);
	fcode3 = makecode4();
	res4 = S4(fcode3);
	printarch("Step4",res4);
	fcode4 = makecode5(res4);
	res5 = S5(fcode4);
	
	
def utfdecode(msg):
	dmsg = msg.decode('utf-8');
	return dmsg;

def printarch(Name,Print):
	FILE = open(Name+".txt","w");
	FILE.write(Print);
	FILE.close();

def makecode(Code,Length,WithPort):
	if(WithPort == True):
		fcode = (Code[:Length]+" 32705");
	else:
		fcode = (Code[:Length]);
		
	#print(fcode);
	return fcode;

def makeUDPsv(IP,PORT):
	sock2=socket(AF_INET,SOCK_DGRAM);
	sock2.bind((IP,PORT));
	return sock2;

def convertOperation(Operation):
	COp = '';

	for i in Operation:
		
		if ((i == '{' )or (i =='[')):
			i = '(';
		elif ((i == '}' )or (i ==']')):
			i = ')';
		#elif (i == '/'):
			#i='//';
		elif (i == ' '):
			i='';
		else:
			i=i;
			
		COp = COp + i;
	
	return(COp);

def chkex(exp):
	counterA = 0;
	counterC = 0;
	for i in exp:
		if(i == '('):
			counterA = counterA + 1;
		elif (i == ')'):
			counterC = counterC +1;

	if(counterA == counterC):
		return True;
	else:
		return False;

def makecode4():
    '''
    Extract from:
    https://stackoverflow.com/questions/2081836/reading-specific-lines-only-python
    '''
    with open("Step3.txt") as fp:
        for i, line in enumerate(fp):
            if i == 5:
                return line;
            elif i > 5:
                break;
    return "";

def makecode5(res4):
    '''
    Extract from:
    https://stackoverflow.com/questions/2081836/reading-specific-lines-only-python
    '''
    with open("Step4.txt") as fp:
        for i, line in enumerate(fp):
            if i == 27:
                return(line[12:17]);
            elif i > 27:
                break;
    return "";
	
def S0():
	sock1=socket(AF_INET);
	#sock1=socket(AF_INET,SOCK_STREAM);
	sock1.connect(("atclab.esi.uclm.es",2000));
	rcv = sock1.recv(1024);
	drcv= utfdecode(rcv);
	#print(drcv);
	return drcv;

def S1(code):
	sv1 = makeUDPsv('',32705);	
	encmsg = code.encode('utf-8')
	dirc=("atclab.esi.uclm.es",2000)
	sock3=socket(AF_INET,SOCK_DGRAM);
	
	sock3.sendto(encmsg,dirc);
	
	#exit=False;
	#while(exit == False):
	rcv=sv1.recv(1024);
	drcv=utfdecode(rcv);
		#if(drcv != ''):
		#	exit= True;
	
	print(drcv);
	return(drcv);

def S2p1(port):
	sock4 = socket(AF_INET);
	dirc = ("atclab.esi.uclm.es",int(port));
	sock4.connect(dirc);
	rstr = S2p2(sock4);		
	print(rstr);
	return(rstr);
	
def S2p2(skt):
	rcv=skt.recv(1024);
		
	drcv=utfdecode(rcv);

	if(drcv[0]=='3'):
		return(drcv);
		
	cdrcv = convertOperation(drcv);
	cond=chkex(cdrcv);
	
	if(cond == False):
		rcvx = skt.recv(1024);
		
		drcvx = utfdecode(rcvx);
		cdrcvx = convertOperation(drcvx);
		
		cdrcv = cdrcv + cdrcvx;
	
	print(cdrcv);
	EvOp=Operator(cdrcv);
	
	EvOpTStr = '(' + str(EvOp) + ')';
	skt.send(EvOpTStr.encode('utf-8'));
		
	return S2p2(skt);

def S3(port):
	sock5 = socket(AF_INET,SOCK_STREAM);
	url = ("atclab.esi.uclm.es",5000); 
	sock5.connect(url);
	
	getstr = "GET /" + port + " HTTP/1.1\r\n\r\n"
	sock5.send(getstr.encode('utf-8'));
	resp1 = sock5.recv(1024).decode();
	resp2 = sock5.recv(2048).decode();
	
	print(resp1);
	print(resp2);
	return(resp1 + resp2);
	
	
def S4(port):
    chksum = 0;
    
    header = struct.pack("BBHHH", 8,0,chksum,os.getpid(),1);
    data = bytes(str(time.clock()).encode() + port.encode());
    chksum = icmp_checksum3.cksum(header+data);
    
    header = struct.pack("BBHHH", 8,0,htons(chksum),os.getpid(),1);
    
    pkt = header+data;
    
    skt = socket(AF_INET,SOCK_RAW,getprotobyname('icmp'));
    skt.sendto(pkt,("atclab.esi.uclm.es",1));
    
    skt.recv(1024);
    insh=skt.recv(2048);
    ins = insh[33:len(insh)];
    insd = utfdecode(ins);
    print(insd);
    return(insd);

#This class and the method below is a copy from:
#https://docs.python.org/2/library/socketserver.html

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data=self.request.recv(1024);
        ddata = data.decode();
        first_line = ddata.split('\n')[0];
        direction=first_line.split(" ")[1];
        opener = urllib.request.FancyURLopener({})
        f=opener.open(direction);
        mens=f.read();
        self.request.sendall(mens);
        print(direction);
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
    
def S5(port):
    port5= port + ' 7322'
    port5=port5.encode('utf-8');
    HOST, PORT = "", 7322
    
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(('atclab.esi.uclm.es', 9000))
    sock.sendall(port5)        
    print(sock.recv(1024).decode('utf-8'))
    
    server.shutdown()
    server.server_close()
    
    #Proxy4.ppal(port);
    
start();
