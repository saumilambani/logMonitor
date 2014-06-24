import os
import time
import datetime 
import Queue
import datetime
import logging
from threading import Event, Thread
from collections import defaultdict
import re

class Reader(Thread):
  """
  The reader thread parses the log file and generates a statistc after every
  monitor interval (10 seconds). It also adds the counts to the queue to be 
  analyzed by the analyzer and sets the processAnEvent 
  """
  def __init__(self, caller):
    Thread.__init__(self)
    self.monitorInterval = caller.monitorInterval
    self.queue = caller.queue
    self.accessLog = caller.accessLog 
    self.stopEvent = caller.stopEvent
    self.processAnEvent = caller.processAnEvent
    self.requestPattern = re.compile(r'\"(.+)\"')
    # Lazy implemntation because we want the first match
    self.sectionPattern = re.compile(r'\/(.+?)\/')
    self.sectionMap = defaultdict(int)
    self.requestMap = defaultdict(int)
    self.count = 0

  def run(self):
    try:
      logging.info("Starting the Reader thread")
      self.tailFile()
      logging.info("Terminating the Reader thread") 
    except Exception, exception:
      self.stopEvent.set()
      print "exception: %s" % exception
 
  def tailFile(self):
    reopen = False
    prevTime = time.time()
    while not self.stopEvent.isSet():
      fh = open(self.accessLog, "r")
      # find the end of the file
      if not reopen: fh.seek(0, os.SEEK_END)
      fstat = os.fstat(fh.fileno())
      line = ""
      while not self.stopEvent.isSet():
        curTime = time.time()
        if curTime - prevTime > self.monitorInterval:
          self.printSummary()
          prevTime = curTime
        else:
          line += fh.readline()
          if line.endswith("\n"):
            self.addCount(line)
            line = ""
          else:
            time.sleep(1)

  def addCount(self, line):
    self.count += 1
    request = re.search(self.requestPattern,line)
    if (request):
      (requestType, path) = request.group().split(' ')
      section = re.search(self.sectionPattern, path)
      if (section):
        sectionAccessed = section.group()[1:-1]
      else:
        sectionAccessed = path[1:]
      self.sectionMap[sectionAccessed] += 1
      self.requestMap[requestType] += 1
    else:
      logging.error("Found no request in line: %s", line)

  def printSummary(self):
    maxSection = self.findMax(self.sectionMap) 
    maxRequestType = self.findMax(self.requestMap)
    print "Stats: In last %.1f sec (TotalHits:%s, MostHitSection:%s,"\
        " MostRequestType:%s) " % (self.monitorInterval,self.count, 
            maxSection, maxRequestType)
    self.queue.append(self.count)
    self.processAnEvent.set() 
    self.count = 0
    self.sectionMap.clear()
    self.requestMap.clear()

  # need to find the most popular section now
  def findMax(self, a_map):
    maxValue = 0
    maxKey = ""
    for k,v in a_map.iteritems():
      if v > maxValue:
        maxValue = v
        maxKey = k
    return maxKey
