import threading, time
import threaded_proximity

if __name__ == "__main__":
    proxThread = threaded_proximity.ThreadedProximity()
    proxThread.start()
    print "Initialized Thread."
    try:
        while True:
            print(proxThread.getNearest())
            time.sleep(2.5)
    except(KeyboardInterrupt, SystemExit):
        proxThread.stop()
        proxThread.join()
        print "Exiting successfully.."