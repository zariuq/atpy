import re
from .. import expres

def mk_pid(pid, name, post):
   return "%s--%s+%s" % (pid, name.replace("/", "+"), post)

def standalone(pid, name):
   proto = expres.protos.load(pid)
   enigma = "1*Enigma(ConstPrio,%s,0.2)" % name
   pid2 = mk_pid(pid, name, "0")
   proto2 = "%s-H'(%s)'" % (proto[:proto.index("-H'")], enigma)
   expres.protos.save(pid2, proto2)
   return pid2

def combined(pid, name, freq=None, mult=0.2):
   proto = expres.protos.load(pid)
   if not freq:
      freq = sum(map(int,re.findall(r"(\d*)\*", proto)))
      post = "S"
   else:
      post = "F%sM%s"%(freq,mult)

   enigma = "%d*Enigma(ConstPrio,%s,%s)" % (freq,name,mult)
   pid2 = mk_pid(pid, name, post)
   proto2 = proto.replace("-H'(", "-H'(%s,"%enigma)
   expres.protos.save(pid2, proto2)
   return pid2

