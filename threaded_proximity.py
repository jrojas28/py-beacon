import sys, time, threading, json
import proximity

class ThreadedCalculator(threading.Thread):
    def __init__(self, calculator = proximity.Calculator(), lock = threading.Lock(), sleepInterval = 0):
        super(ThreadedCalculator, self).__init__()
        self.calculator = calculator
        self.lock = lock 
        self.sleepInterval = sleepInterval
        self.__stopEvent  = threading.Event()

    # ------------------- Threading Related Functions -----------------------
    def run(self):
        while not self.isStopped():
            bid, rssi = self.nearest()
            if bid:
                #Something must happen with the bid, for instance, sending it to someone.
                print "Nearest: " + str(bid)
                print "Average RSSI For Nearest: " + str(rssi)
            if self.sleepInterval != 0:
                print "Sleeping for " + str(self.sleepInterval) + " seconds."
                time.sleep(self.sleepInterval)
        print "Finishing Threaded Calculator..."
        sys.exit()
                
    def stop(self):
        print "Stopping Thread..."
        self.__stopEvent.set()

    def isStopped(self):
        return self.__stopEvent.is_set()
    # -----------------------------------------------------------------------

    def add(self, json):
        self.lock.acquire()
        try:
            jsonObj = json.loads(data)
            self.calculator.add(obj["id"], int(obj["rssi"]))   
        finally:
            self.lock.release()
    
    def nearest(self):
        self.lock.acquire()
        try:
            bid, rssi = self.calculator.nearest()
        finally:
            self.lock.release()
        if bid:
            return (bid, rssi)
        return None, None

class ThreadedScanner(threading.Thread):
    def __init__(self, scanner = proximity.Scanner(), lock = threading.Lock(), sleepInterval = 0):
        super(ThreadedScanner, self).__init__()
        self.scanner = scanner
        self.lock = lock 
        self.sleepInterval = sleepInterval
        self.__stopEvent  = threading.Event()

    # ------------------- Threading Related Functions -----------------------
    def run(self):
        while not self.isStopped():
            bid, rssi = self.nearest()
            if bid:
                #Something must happen with the bid, for instance, sending it to someone.
                print "Nearest: " + str(bid)
                print "Average RSSI For Nearest: " + str(rssi)
            if self.sleepInterval != 0:
                print "Sleeping for " + str(self.sleepInterval) + " seconds."
                time.sleep(self.sleepInterval)
        print "Finishing Threaded Calculator..."
        sys.exit()
                
    def stop(self):
        print "Stopping Thread..."
        self.__stopEvent.set()

    def isStopped(self):
        return self.__stopEvent.is_set()
    # -----------------------------------------------------------------------
    def scan(self):
        self.lock.acquire()
        try:
            beacons = self.scanner.scan()
        finally:
            self.lock.release()
        if beacons:
            return beacons
        return none

class ThreadedProximity(threading.Thread):
    def __init__(self, scanner = proximity.Scanner(), calculator = proximity.Calculator(), sleepInterval = 0):
        super(ThreadedProximity, self).__init__()
        self.__stopEvent  = threading.Event()
        self.__scanner = scanner
        self.__calculator = calculator
        self.__sleepInterval = sleepInterval

    # ------------------- Threading Related Functions -----------------------
    def run(self):
        while not self.isStopped():   
            for beacon in self.__scanner.scan():
                fields = beacon.split(",")
                #Reference:
                # fields[0] = MAC Address 
                # fields[1] = UDID
                # fields[2] = Major
                # fields[3] = Minor
                # fields[4] = Unknown (DONT USE)
                # fields[5] = RSSI
                values = {'mac': fields[0], 'bid': fields[1], 'major': int(fields[2]), 'minor': int(fields[3]), 'rssi': int(fields[5]) }
                self.__calculator.add(values['mac'], values['rssi'], values['major'], values['minor'])
            if self.__sleepInterval != 0:
                time.sleep(self.__sleepInterval)
        print "Finishing Threaded Proximity Manager..."
        sys.exit()
    
    def getNearest(self):
        return self.__calculator.nearest()
                
    def stop(self):
        print "Stopping Thread..."
        self.__stopEvent.set()

    def isStopped(self):
        return self.__stopEvent.is_set()
    # -----------------------------------------------------------------------