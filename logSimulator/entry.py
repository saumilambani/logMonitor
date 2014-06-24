"""
Class to create a random log entry for access log. 

The print format for Entry is based on 
http://www.w3.org/Daemon/User/Config/Logging.html#AccessLog:
remotehost rfc931 authuser [date] "request" status bytes
e.g. 128.7.2.1 neymar robben [23/06/2014:01:09:18 -0-5.000] "PUT /photos/gallery2" 500 130
"""

import time, random
from math import floor

hosts=["195.3.2.1", "128.7.2.1","3.2.5.3"]
rfc931=["-","messi","ronaldo","neymar"]
authuser=["-","dempsey","robben","balotelli"]
methods=["GET", "DELETE", "PUT", "POST"]
status=["200","301","400","404","500"]
path=["/about", "/travel", "/travel/peru", "/travel/mexico", "/travel/france"
    ,"/photos", "/photos/gallery1", "/photos/gallery2"]

# date format function used from :
# https://github.com/bunelr/HTTP-log-monitoring-console-program/blob/master/log_generator/log_fields.py
def getZeroPaddedUTCOffset():
    nbHours=floor((time.mktime(time.localtime())-time.mktime(time.gmtime()))/3600)
    sign="+" if nbHours>=0 else "-"
    value="0"+str(nbHours) if nbHours<10 else str(nbHours)
    return sign+value+"00"
 
class Entry(object):
  """A class to generate a random log entry """
  def __init__(self):
     self.method = random.choice(methods)
     self.remoteHost = random.choice(hosts) 
     self.remoteLogName = random.choice(rfc931) 
     self.remoteUserName = random.choice(authuser)
     self.status = random.choice(status)
     self.path = random.choice(path)
     now = time.gmtime()
     self.now = time.strftime("%d/%m/%Y:%H:%M:%S ", now)+getZeroPaddedUTCOffset() 
     self.bytes = random.randrange(10,3000,1)

  def __str__(self):
     return '%s %s %s [%s] "%s %s" %s %s\n' % (self.remoteHost, self.remoteLogName, self.remoteUserName, 
           self.now, self.method, self.path, self.status, self.bytes)
