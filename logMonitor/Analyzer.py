import time
import datetime
import ConfigParser
import CountMetric
from threading import Event, Thread
import LogParser
import Analyzer
import collections
import colorama
import logging
from colorama import Fore, Back, Style

class Analyzer(Thread):
  
  """
  This thread calculates the average traffic per second over the windowSize 
  (2 min). It generates an alert every time the threshold is breacheed and 
  when the average traffic returns back to below the threshold
  """

  def __init__(self, caller):
    Thread.__init__(self)
    self.stopEvent = caller.stopEvent
    self.queue = caller.queue
    self.threshold = caller.threshold
    self.monitorInterval = caller.monitorInterval
    self.windowSize = caller.windowSize
    self.thresholdBreached = False
    self.processAnEvent = caller.processAnEvent
    logging.info(" Initializing Analyzer")

  def run(self):
    try:
      logging.info("Starting the Analyzer thread")
      colorama.init()
      while not self.stopEvent.isSet():
        if self.processAnEvent.isSet():
          logging.debug("Queue is " + str(self.queue))
          self.checkTraffic()
          self.processAnEvent.clear()
        else:
          time.sleep(1)
      logging.info("Terminating the Analyzer thread")
    except Exception, exception:
      self.stopEvent.set()
      print "exception: %s" % exception

  def checkTraffic(self):
    queueList = list(self.queue)
    avgTraffic = float(sum(queueList))/self.windowSize
    logging.debug("Average traffic = %.2f , Threshold = %.2f \n",avgTraffic, 
        self.threshold)  
    
    if (self.thresholdBreached == False and avgTraffic > self.threshold):
      text = "High traffic generated an alert - avgHits/second = {%f} "\
          "trigerred at %s " % (avgTraffic, datetime.datetime.now())
      print(Fore.RED + text + Style.RESET_ALL)
      self.thresholdBreached = True
    elif (self.thresholdBreached == True and avgTraffic < self.threshold):
      text = "Traffic recovered - avgHits/sec = {%f} trigerred at "\
          "%s" % (avgTraffic, datetime.datetime.now())
      print(Fore.GREEN + text + Style.RESET_ALL)
      self.thresholdBreached = False
