import re
import sha
from os import path, system, getenv

from .runner import Runner
from atpy import eprover

E_PROTO_ARGS = "--definitional-cnf=24 %(splaggr)s %(splcl)s %(srd)s %(simparamod)s %(forwardcntxtsr)s --destructive-er-aggressive --destructive-er --prefer-initial-clauses -t%(tord)s %(prord)s -F1 --delete-bad-limit=150000000 -W%(sel)s %(sine)s %(heur)s"
      
#E_SINE_ARGS = "--sine='GSinE(CountFormulas,%(sineh)s,%(sinegf)s,,%(sineR)s,%(sineL)s,1.0)'"

E_SINE_ARGS = "--sine='GSinE(%(sineG)s,%(sineh)s,%(sinegf)s,%(sineD)s,%(sineR)s,%(sineL)s,%(sineF)s)'"

def cef2block(cef):
   "Encode a CEF as a ParamILS string containg only [a-zA-Z0-9_]."
   return cef.replace("-","_M_").replace(",","__").replace(".","_D_").replace("(","__").replace(")","")

def block2cef(block):
    "Decode a CEF from a ParamILS string."
    parts = block.replace("_M_","-").replace("_D_",".").split("__")
    return "%s(%s)" % (parts[0],  ",".join(parts[1:]))
   
SINE_DEFAULTS = { 
   "sineG": "CountFormulas", 
   "sineh": "hypos", 
   "sinegf": "1.2",
   "sineD": "none", 
   "sineR": "none", 
   "sineL": "100",
   "sineF": "1.0" 
}

def convert(params):
   # conversion from old ordering version
   if "prord" in params:
      params = dict(params)
      params["tord_prec"] = params["prord"]
      if params["tord"] == "KBO6":
         params["tord_weight"] = "invfreqrank"
         params["tord_const"] = "1"
      del params["prord"]
   # handle old sine version
   if "sine" in params and params["sine"] == "1":
      if params["sineR"] == "UU":
         params["sineR"] = "none" 
      defaults = dict(SINE_DEFAULTS)
      defaults.update(params)
      params = defaults
   else:
      params["sine"] = "0"

   return params

class EproverRunner(Runner):
   def __init__(self, direct=True, cores=4):
      Runner.__init__(self, direct, cores)
      self.conf_prefix = "conf_eprover_"
      self.conf_dir = "confs"
      if not direct:
         system("mkdir -p %s" % self.conf_dir)

   def cmd(self, params, inst, limit=None, extra=None):
      args = self.args(params)
      d_root = getenv("TPTP", ".") # probably not needed!
      return eprover.runner.cmd(path.join(d_root,inst), args, limit)
   
   def args(self, params):
      eargs = dict(params)
      eargs = convert(eargs)
      # global params
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
      # term ordering
      if eargs["tord"] == "KBO6":
         eargs["prord"] = "-G%(tord_prec)s -w%(tord_weight)s" % eargs
         if eargs["tord_const"] != "0":
            eargs["prord"] += " -c%(tord_const)s" % eargs
      elif eargs["tord"] == "LPO4":
         eargs["prord"] = "-G%(tord_prec)s" % eargs
      else:
         eargs["prord"] = ""
      # SinE
      if eargs["sine"] == "1":
         for x in eargs:
            if x.startswith("sine") and eargs[x] == "none":
               eargs[x] = ""
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
   
   #def quality(self, out):
   #   result = eprover.result.parse(None, out=out)
   #   if eprover.result.solved(result):
   #      #return result["MILINS"] if "MILINS" in result else None
   #      return result["PROCESSED"] if "PROCESSED" in result else None
   #   elif eprover.result.error(result):
   #      print out
   #      return None
   #   else:
   #      return 1000000

   #def clock(self, out):
   #   result = eprover.result.parse(None, out=out)
   #   return result["RUNTIME"] if "RUNTIME" in result else None

   def process(self, out, inst, limit, result=None):
      if not result:
         result = eprover.result.parse(None, out=out)
      if eprover.result.error(result):
         return None

      runtime = result["RUNTIME"] if "RUNTIME" in result else limit
      quality = result["PROCESSED"] if eprover.result.solved(result) else 1000000
      return [quality, runtime]
         
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
      
      if "sine" in params and params["sine"] == "0":
         delete.extend(SINE_DEFAULTS)

      if "prord" not in params:
         if params["tord"] == "Auto":
            delete.extend(["tord_prec", "tord_weight", "tord_const"])
         elif params["tord"] == "LPO4":
            delete.extend(["tord_weight", "tord_const"])
      
      for param in delete:
         if param in params:
            del params[param]

      return params

