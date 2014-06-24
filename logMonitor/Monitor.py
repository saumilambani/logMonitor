import logging
import time
import ConfigParser
from threading import Event, Thread
import collections

import LogParser
import Analyzer

class Monitor(Thread):
  
  """
  The monitor thread reads from the configuration file the monitoring interal
  and the windowSize to create a queue of fixed length. This fixed length will
  ensure that the queue only holds informtion required for the size of the 
  window. The monitor thread creates a reader thread, which parses the log files
  and an analytics thread which evaluates the queue to decide if an alert 
  should be gerenated. 
  """

  def __init__(self, caller):
    Thread.__init__(self)
    logging.info("Initializing monitor thread")
    self.config = caller.config
    self.setConfig()
    self.queue = collections.deque(maxlen=self.queueLen)
    logging.debug("Size of the fixed queue is %d", self.queueLen)
    self.stopEvent = caller.stopEvent
    self.processAnEvent = Event()
    self.reader = LogParser.Reader(self)
    self.analyzer = Analyzer.Analyzer(self)
  
  def setConfig(self):
    self.accessLog = self.config.get('AccessLog', 'location')
    self.windowSize = self.config.getfloat('Monitor', 'windowSize')
    self.threshold = self.config.getfloat('Monitor', 'threshold')
    self.monitorInterval = self.config.getfloat('Monitor', 'monitorInterval')
    self.queueLen = int(self.windowSize)/int(self.monitorInterval)  
    logging.debug("Monitor() queue length is %d", self.queueLen)

  def run(self):
    try:
      logging.info("Starting monitor thread")
      startTime = time.time()
      self.reader.start()
      self.analyzer.start()
      while not self.stopEvent.isSet():
        time.sleep(1)
      self.reader.join()
      self.analyzer.join()
      logging.info("Terminating the monitor thread")

    except Exception, exception:
      print "exception: %s" % exception
      self.stopEvent.set()
      self.reader.join()
      self.analyzer.join()
      logging.info("Terminating the monitor thread due to exception")

if __name__ == '__main__':
  print "Initiating Log Monitor"
  monitor = Monitor()
  monitor.start()
