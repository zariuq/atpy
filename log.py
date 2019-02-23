from datetime import datetime

def msg(msg, first=[], prefix="~~~ atpy runlog ~~~ "):
   now = datetime.now()
   if not first:
      first.append(now)
   
   msg = "[%s] %s" % (now-first[0], msg)
   print msg
   if prefix:
      f = file(prefix+str(first[0]),"a")
      f.write(msg+"\n")
      f.flush()
      f.close()

