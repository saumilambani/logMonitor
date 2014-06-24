import logging
import time
from threading import Event, Thread
import ConfigParser
import argparse 

import Monitor

CONFIG_FILE = "console.cfg"

"""
Threads:
                               WatchDog (main)
                                  |
                                Monitor
                                  | 
                             ------------
                             |           |
                           Reader     Analyzer

"""

class WatchDog(object):

  """
  Watchdog is the main thread which sets up logging and checks for the duration 
  for which the watch dog should run. It creates a monitor thread. The 
  watchdog in future can expand to incorporate other functionalities. If 
  duration is specified, watchdog gracefully exits at the end of the duration
  else waits for a keyboard interrupt, at which point it waits for all 
  the threads to join and then gracefully exit
  """
  
  def __init__(self):
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)
    self.config = config
    logLocation = config.get('Monitor', 'monitorLogLocation')
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
      datefmt='%m/%d/%Y %H:%M:%S',
      filename=logLocation, 
      level=logging.DEBUG)

    # This event is responsible for stopping all the threads 
    self.stopEvent = Event()
    # Initialize a monitor thread
    self.monitor = Monitor.Monitor(self)
    logging.info("Initialized watchdog")
    
  def start(self):
    try:
      startTime = time.time()
      self.monitor.start()
      while not self.stopEvent.isSet():
        time.sleep(1)
        if ((self.duration is not None) and 
            (time.time()-startTime)>float(self.duration)):
          logging.debug("Watchdog completed given duration of %s", 
              self.duration)
          self.stopEvent.set()
          self.monitor.join()
      logging.info("Exiting watchdog")
    
    except KeyboardInterrupt:
      print "Keyboard Interrupt"
      self.stopEvent.set()
      self.monitor.join()

if __name__ == '__main__':
  parser=argparse.ArgumentParser()
  parser.add_argument("--dur", help="Duration for which watchdog should run")
  args=parser.parse_args()
  watchdog = WatchDog()
  watchdog.duration = args.dur
  watchdog.start()
