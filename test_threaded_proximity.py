import threading
from threaded_proximity import *

if __name__ == "__main__":
    proxThread = threaded_proximity.ThreadedProximity()
    print "Initialized Thread."
    try:
        while True:
            print(proxThread.getNearest())
    except(KeyboardInterrupt, SystemExit):
        proxThread.stop()
        proxThread.join()
        print "Exiting successfully.."