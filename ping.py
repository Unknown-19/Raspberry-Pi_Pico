import urequests as requests
import ujson as json
import socket
import machine
import network
import time
import gc

led = machine.Pin('LED', machine.Pin.OUT)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# Connect Wifi
ssid = ''
password = ''
wlan.connect(ssid, password)
led.on()
time.sleep(10)
led.off()


def ping():
    webhook_url = ""


    ICM_Type = (0x08)
    ICM_Code = (0x00)
    ICM_ID = (0x01)
    ICM_Seq = (0x01)
    ICM_LIST = [0]*6
    
    ICM_LIST[0] = ICM_Type
    ICM_LIST[1] = ICM_Code
    ICM_LIST[2] = 0
    ICM_LIST[3] = 0
    ICM_LIST[4] = ICM_ID
    ICM_LIST[5] = ICM_Seq
    ICM_DATA = b"ping"
    ICM_LIST.extend(ICM_DATA)
    csum = 0
    for i in range(int(len(ICM_LIST)/2)):
	    csum += (ICM_LIST[i*2]<<8) | (ICM_LIST[i*2+1])
    csum = (csum&0xffff) + (csum>>16)
    csum = 0xffff-(csum)
     
    #print("ChekeSum: " + hex(csum))
    ICM_LIST[2] = (csum&0xFF00)>>8
    ICM_LIST[3] = csum&0x00FF
    #print(bytes(ICM_LIST))
    
    IP = []
    for i in range(1, 17):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, 1)
        IPaddr = f"192.168.0.{i}"
        sock.sendto(bytes(ICM_LIST), (IPaddr, 0))
        sock.settimeout(1)
        gc.collect()
        try:
            data = sock.recv(255)
            IP.append(IPaddr)
        except:
            pass
    embed_data = {"embeds": [
            {
                "title": "IP List",
                "description": '\n'.join(IP),
                "color": 000000,
            }
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    requests.post(webhook_url, data=json.dumps(embed_data), headers=headers)
    
    print('\n'.join(IP))
while True:
    ping()
    time.sleep(30)
    #data = sock.recv(255)

#for i in range(20,len(data)):
#    print ("%r" % hex(data[i])),
#print(data)
