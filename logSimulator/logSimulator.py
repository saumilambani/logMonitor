"""
This module generates a mock W3 formatted HTTP access log generator
"""
import argparse
from time import sleep
import logging
import random
import ConfigParser
import time

import entry

CONFIG_FILE = "console.cfg"

def logSimulator():
  """
  Main function for generating the logs. Generates randomized log entries
  to access log 
  """
  
  config = ConfigParser.RawConfigParser()
  config.read(CONFIG_FILE)
  logLocation = config.get('Simulator', 'simLogLocation')
  logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%m/%d/%Y %H:%M:%S',
    filename=logLocation, 
    level=logging.DEBUG)

  parser=argparse.ArgumentParser()
  parser.add_argument("--numLines", help="Number of lines to be generated")
  args=parser.parse_args()

  accessLogFile = config.get('AccessLog','location')
  with open(accessLogFile,'w') as logFile:
    if args.numLines is None:
      logging.info("Beginning log generation")
      while True:
        addEntry(logFile)
        sleep(genLogInterval())
    else:
      logging.info("Generating %s lines of log", args.numLines)
      for _ in range(int(args.numLines)):
        addEntry(logFile)
        sleep(genLogInterval())
  return 0

def addEntry(logFile):
  """
  Generates a randomized log entry and writes it to accessLog File
  """
  accessEntry = str(entry.Entry())
  logFile.write(accessEntry)
  logFile.flush()
  # Change to print (accessEntry,end="") for python3 
  print (accessEntry),

def genLogInterval():
  """
  Generates a varying time interval between two log messages. There are 
  two components for the interval: a varying deterministic component and 
  a random component. New test scenarios can be incorporated here. 
  """
  # (time.time())%60/60.0 will keep increasing to 1 and
  # then reset to zero every 60 seconds. This should enable testing both 
  # high traffic alert and coming back to regular traffic scenario
  detVal =  (time.time())%60/60.0 # value between 0 and 1
  ranVal = random.random()/2.0 # scaling down the random value  
  interval = detVal + ranVal
  logging.debug("genLogInterval() (Det:%f, Ran:%f)", 
      detVal, ranVal)
  return interval

if __name__ == '__main__':
  logSimulator() 

