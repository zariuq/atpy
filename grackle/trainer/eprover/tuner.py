from os import system, path
from atpy import paramils
from atpy.grackle.runner.eprover import EproverRunner
from . import domain


SCENARIO = """
algo = %s
execdir = .
deterministic = 1
run_obj = runlength
overall_obj = mean
cutoff_time = %s
cutoff_length = max
tunerTimeout = %s
paramfile = params.txt
outdir = paramils-out
instance_file = instances.txt
test_instance_file = empty.tst
"""

def launch(scenario, domains, init, insts, cwd, timeout, cores):
   system("rm -fr %s" % cwd)
   system("mkdir -p %s" % cwd)

   f_scenario = path.join(cwd, "scenario.txt")
   f_params = path.join(cwd, "params.txt")
   f_instances = path.join(cwd, "instances.txt")
   f_empty = path.join(cwd, "empty.tst")
   f_init = path.join(cwd, "init_00")
   
   file(f_scenario,"w").write(scenario)
   file(f_params,"w").write(domains)
   file(f_instances,"w").write("\n".join(insts))
   file(f_empty,"w").write("")
   file(f_init,"w").write(" ".join(["%s %s"%(x,init[x]) for x in sorted(init)]))

   params = paramils.reparamils.run_reparamils(
      "scenario.txt",
      path.join(cwd,"paramils-out"),
      cwd,
      count=cores,
      N=len(insts),
      validN=str(len(insts)),
      init="init_00",
      #out=None,
      out=file(path.join(cwd,"paramils.out"),"w"),
      time_limit=timeout)

   return params

class Tuner(EproverRunner):
   def __init__(self, direct, cores, nick, cls):
      EproverRunner.__init__(self, direct)
      self.nick = nick
      self.cls = cls

   def split(self, params):
      pass

   def join(self, main, extra):
      pass

   def domains(self, config, init=None):
      pass

class BaseTuner(Tuner):
   def __init__(self, direct, cores=4):
      Tuner.__init__(self, direct, cores, "0-base", "atpy.grackle.trainer.eprover.tuner.BaseTuner")

   def split(self, params):
      return (params, None)

   def join(self, main, extra):
      return main

   def domains(self, config, init=None):
      return domain.base(config, init=init)

BASE = BaseTuner(True, 1)

