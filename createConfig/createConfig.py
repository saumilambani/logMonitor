import ConfigParser
import logging
import sys

def createConfig():
  config = ConfigParser.RawConfigParser()

  # Access log 
  config.add_section('AccessLog')
  # Location
  config.set('AccessLog', 'location', "data/accessLog.txt")

  # Simulator configuration
  config.add_section('Simulator')
  # Location of log files
  config.set('Simulator', 'simLogLocation', "logs/simulator.log")

  # Monitor configuration
  config.add_section('Monitor')
  # Interval to find top section (seconds)
  config.set('Monitor', 'monitorInterval', 10.0)
  # Window to be considered for traffic alerts (seconds)
  config.set('Monitor', 'windowSize', 120.0)
  # Threshold for high traffic (requests per second) alert
  config.set('Monitor', 'threshold', 1.5)
  # Location of log files
  config.set('Monitor', 'monitorLogLocation',"logs/monitor.log")

  with open('console.cfg', 'wb') as configfile:
    config.write(configfile)

if __name__ == '__main__':
  createConfig()
