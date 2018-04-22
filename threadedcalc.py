import time, threading, json
from proximity import Calculator

class ThreadedCalculator(threading.Thread):
    def __init__(self, calculator = Calculator(), lock = threading.Lock(), sleepInterval = 0):
        super(ThreadedCalculator, self).__init__()
        self.calculator = calculator
        self.lock = lock 
        self.sleepInterval = sleepInterval
        self._stopEvent  = threading.Event()

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
                time.sleep(sleepInterval)
        print "Finishing Threaded Calculator..."
        return
                
    def stop(self):
        print "Stopping Thread..."
        self._stopEvent.set()

    def isStopped(self):
        return self._stopEvent.is_set()
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

