import re
import sha
from os import path, system

from .runner import Runner
from atpy import eprover

E_PROTO_ARGS = "--definitional-cnf=24 %(splaggr)s %(splcl)s %(srd)s %(simparamod)s %(forwardcntxtsr)s --destructive-er-aggressive --destructive-er --prefer-initial-clauses -t%(tord)s %(prord)s -F1 --delete-bad-limit=150000000 -W%(sel)s %(sine)s %(heur)s"
      
E_SINE_ARGS = "--sine='GSinE(CountFormulas,%(sineh)s,%(sinegf)s,,%(sineR)s,%(sineL)s,1.0)'"

def cef2block(cef):
   "Encode a CEF as a ParamILS string containg only [a-zA-Z0-9_]."
   return cef.replace("-","_M_").replace(",","__").replace(".","_D_").replace("(","__").replace(")","")

def block2cef(block):
    "Decode a CEF from a ParamILS string."
    parts = block.replace("_M_","-").replace("_D_",".").split("__")
    return "%s(%s)" % (parts[0],  ",".join(parts[1:]))

class EproverRunner(Runner):
   def __init__(self, direct=True, cores=4):
      Runner.__init__(self, direct, cores)
      self.conf_prefix = "conf_eprover_"
      self.conf_dir = "confs"
      system("mkdir -p %s" % self.conf_dir)

   def cmd(self, params, inst, limit=None):
      args = self.args(params)
      return eprover.runner.cmd(inst, args, limit)
   
   def args(self, params):
      eargs = dict(params)
      # default params
      eargs["splaggr"] = "--split-aggressive" if eargs["splaggr"] == "1" else ""
      eargs["srd"] = "--split-reuse-defs" if eargs["srd"] == "1" else ""
      eargs["forwardcntxtsr"] = "--forward-context-sr" if eargs["forwardcntxtsr"] == "1" else ""
      eargs["splcl"] = "--split-clauses="+eargs["splcl"] if eargs["splcl"]!="0" else ""
      if eargs["simparamod"] == "none":
         eargs["simparamod"] = ""
      elif eargs["simparamod"] == "oriented":
         eargs["simparamod"] = "--oriented-simul-paramod"
      else:
         eargs["simparamod"] = "--simul-paramod"
      if eargs["prord"] == "invfreq":
         eargs["prord"] = "-winvfreqrank -c1 -Ginvfreq"
      else:
         eargs["prord"] = "-G" + eargs["prord"]
      # SinE
      if eargs["sine"] == "1":
         eargs["sineh"] = "" if eargs["sineh"] == "none" else eargs["sineh"]
         eargs["sineR"] = "" if eargs["sineR"] == "UU" else eargs["sineR"]
         eargs["sine"] = E_SINE_ARGS % eargs
      else:
         eargs["sine"] = ""
      # heuristic
      slots = int(eargs["slots"])
      cefs = []
      for i in range(slots):
         cefs += ["%s*%s" % (eargs["freq%d"%i],block2cef(eargs["cef%d"%i]))]
      cefs.sort()
      eargs["heur"] = "-H'(%s)'" % ",".join(cefs)
      return E_PROTO_ARGS % eargs
   
   def quality(self, out):
      result = eprover.result.parse(None, out=out)
      if eprover.result.solved(result):
         return result["MILINS"] if "MILINS" in result else None
      else:
         return 1000000

   def clock(self, out):
      result = eprover.result.parse(None, out=out)
      return result["RUNTIME"] if "RUNTIME" in result else None

   def name(self, params):
      args = self.repr(params).replace("="," ")
      conf = self.conf_prefix+sha.sha(args).hexdigest()
      file(path.join(self.conf_dir,conf),"w").write(args)
      return conf

   def recall(self, conf):
      args = file(path.join(self.conf_dir,conf)).read().strip()
      return self.params(args.split())
  
   def clean(self, params):
      """Remove unused slots from params
      
      This is, however, not usually done, because unused parameters can become 
      used again and their values are set to defaults, possibly reseting 
      usefull values.
      """

      if not "slots" in params:
         return None
      params = dict(params)
      slots = int(params["slots"])
      delete = []
      for param in params:
         if param.startswith("freq") or param.startswith("cef"):
            n = int(param.lstrip("freqcef"))
            if n >= slots:
               delete.append(param)
      for param in delete:
         del params[param]

      return params

