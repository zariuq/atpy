import re
from .. import expres

def standalone(pid, name, mult=0, noinit=False):
   proto = expres.protos.load(pid)
   enigma = "1*Enigma(ConstPrio,%s,%s)" % (name, mult)
   eproto = "%s-H'(%s)'" % (proto[:proto.index("-H'")], enigma)
   post = "0M%s" % mult
   if noinit:
      eproto = eproto.replace("--prefer-initial-clauses", "")
      post += "No" 
   epid = "Enigma+%s+%s+%s" % (name.replace("/","+"), pid, post)
   expres.protos.save(epid, eproto)
   return epid

def combined(pid, name, freq=None, mult=0, noinit=False):
   proto = expres.protos.load(pid)
   if not freq:
      freq = sum(map(int,re.findall(r"(\d*)\*", proto)))
      post = "S"
   else:
      post = "F%s"% freq
   post += "M%s" % mult
   enigma = "%d*Enigma(ConstPrio,%s,%s)" % (freq,name,mult)
   eproto = proto.replace("-H'(", "-H'(%s,"%enigma)
   if noinit:
      eproto = eproto.replace("--prefer-initial-clauses", "")
      post += "No"
   epid = "Enigma+%s+%s+%s" % (name.replace("/","+"), pid, post)
   expres.protos.save(epid, eproto)
   return epid

