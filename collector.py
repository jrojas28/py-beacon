#
# by Taka Wang
#

import socket
import ConfigParser
from proximity import *

DEBUG = True

def sendData(socket, target, data):
    socket.sendto(data, (target))

def receiveData(socket):
    data, addr = socket.recvfrom(1024)
    return (data, addr)

def initSocket(receiveAddress = ('', 9876)):
    """Init Socket Listener connection"""
    try:
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.bind(receiveAddress)
        return udpSocket
    except Exception, e:
        print(e)
        return None

def startScan(socket, sendAddress = ('127.0.0.1', 9870), filter="", topic="/ble/rssi/"):
    """Scan BLE beacon and publish to Socket Server"""
    if socket:
        scanner = Scanner()
        if DEBUG:
            print "Started Scanning, reporting to " + str(sendAddress[0]) + ":" + str(sendAddress[1])
        while True:
            for beacon in scanner.scan():
                fields = beacon.split(",")
                #Reference:
                # fields[0] = MAC Address 
                # fields[1] = UDID
                # fields[2] = Major
                # fields[3] = Minor
                # fields[4] = Unknown (DONT USE)
                # fields[5] = RSSI
                if fields[1].startswith(filter):
                    sendData(socket, sendAddress, '{"id":"%s","rssi":"%s"}' % (fields[0], fields[5]))
                    if DEBUG: 
                        print('{"id":"%s","rssi":"%s"}' % (fields[0], fields[5]))
                        print('{"major":"%s","minor":"%s"' % (fields[2], fields[3]))

def init():
    """Read config file"""
    ret = {}
    config = ConfigParser.ConfigParser()
    config.read("config")
    global DEBUG
    DEBUG = True if int(config.get('Collector', 'debug')) == 1 else False
    ret["send_url"]         = config.get('Collector', 'send_url')
    ret["send_port"]        = int(config.get('Collector', 'send_port'))
    ret["receive_url"]      = config.get('Collector', 'receive_url')
    ret["receive_port"]     = int(config.get('Collector', 'receive_port'))
    ret["filter"]           = config.get('Scanner', 'filter')
    ret["topic_id"]         = config.get('Scanner', 'topic_id')
    return ret

if __name__ == '__main__':
    conf = init()
    if DEBUG:
        print "Config Initialized."
    socket = initSocket((conf["receive_url"], conf["receive_port"]))
    if DEBUG:
        print "Socket initialized."
    sendAddress = (conf["send_url"], conf["send_port"])
    startScan(socket, sendAddress, conf["filter"], conf["topic_id"])
