#
# by Taka Wang
#
import select, time, ConfigParser, json
from proximity import *

DEBUG = True
calculator = 0
conf  = 0

def sendData(socket, target, data):
    socket.sendto(data, (target))

def receiveData(socket):
    data, addr = socket.recvfrom(1024)
    return (data, addr)
    
def initSocket(receiveAddress = ('', 9870)):
    """Init Socket Listener connection"""
    try:
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udpSocket.bind(receiveAddress)
        return udpSocket
    except Exception, e:
        print(e)
        return None

def init():
    """Read config file"""
    ret = {}
    config = ConfigParser.ConfigParser()
    config.read("config")
    global DEBUG
    DEBUG = True if int(config.get('Emitter', 'debug')) == 1 else False
    ret["send_url"]         = config.get('Emitter', 'send_url')
    ret["send_port"]        = int(config.get('Emitter', 'send_port'))
    ret["receive_url"]      = config.get('Emitter', 'receive_url')
    ret["receive_port"]     = int(config.get('Emitter', 'receive_port'))
    ret["queueCapacity"]    = int(config.get('Calculator', 'queueCapacity'))
    ret["chkTimer"]         = int(config.get('Calculator', 'chkTimer'))
    ret["threshold"]        = int(config.get('Calculator', 'threshold'))
    ret["topic_id"]         = config.get('Scanner', 'topic_id')
    ret["nearest_id"]       = config.get('Scanner', 'nearest_id')
    ret["topic_id_len"]     = len(ret["topic_id"])
    ret["sleepInterval"]    = int(config.get('Emitter', 'sleepInterval'))
    return ret

if __name__ == '__main__':
    conf = init()
    calculator = Calculator(conf["queueCapacity"], conf["chkTimer"], conf["threshold"])
    if DEBUG:
        print "Config Initialized."
    udpSocket = initSocket((conf["receive_url"], conf["receive_port"]))
    if DEBUG:
        print "Socket initialized."
    sendAddress = (conf["send_url"], conf["send_port"])

    inputSockets = [udpSocket]
    writableSockets = []
    
    while True:
        readable, writable, exceptional = select.select(inputSockets, writableSockets, inputSockets, 0)
        if len(readable) > 0:
            print "Found data on UDP Socket."
        else 
            print "No data received."
        for socket in readable
            if socket is udpSocket
                data, addr = receiveData(udpSocket)
                if DEBUG:
                    print "Received data from " + str(addr)
                    print "Data received: " + str(data)
                obj = json.loads(data)
                calculator.add(obj["id"], int(obj["rssi"]))                
        if DEBUG:
            print "Sleeping for " + str(conf["sleepInterval"])
        time.sleep(conf["sleepInterval"])
        if DEBUG:
            print "Calculating for nearest..."
        ret, val = calculator.nearest()
        if ret:
            sendData(socket, sendAddress, str('{"id":"%s","rssi":"%s"}' % (ret, val)))
            if DEBUG: 
                print "Nearest: " + str(ret, val)
        