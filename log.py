from datetime import datetime

def msg(msg, first=[]):
   if not first:
      first.append(datetime.now())
   print "[%s] %s" % (datetime.now()-first[0], msg)

