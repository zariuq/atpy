import re
import sha
from os import path, system

from .runner import Runner
from atpy import eprover

class EproverRunner(Runner):
   RESULT = re.compile(r"Auc: ([01]\.[0-9]*)")

   def __init__(self, direct=True, cores=4):
      Runner.__init__(self, direct, cores)
      self.conf_prefix = "conf_eprover_"
      self.conf_dir = "confs"
      system("mkdir -p %s" % self.conf_dir)

   def cmd(self, params, inst, limit=None):
      args = self.args(params)
      return eprover.runner.cmd(inst, args, limit)
   
   def args(self, params):
      # TODO
      return " ".join(["-%s %s"%(p,params[p]) for p in sorted(params)])
   
   def quality(self, out):
      # TODO
      q = Runner.quality(self, out)
      return int(10000*(1.0-float(q))) if q else None

   def clock(self, out):
      # TODO
      c = Runner.clock(self, out)
      return int((float(c)/1000.0)*1000)/1000.0 if c else None

   def name(self, params):
      args = self.repr(params).replace("="," ")
      conf = self.conf_prefix+sha.sha(args).hexdigest()
      file(path.join(self.conf_dir,conf),"w").write(args)
      return conf

   def recall(self, conf):
      args = file(path.join(self.conf_dir,conf)).read().strip()
      return self.params(args.split())
  
   def clean(self, params):
      # TODO
      return params
