from os import path, system
from ..trainer import Trainer
from atpy import paramils
from .params import simple


SCENARIO = """
algo = grackle-wrapper.py %s
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

class EproverSimpleTrainer(Trainer):
   def __init__(self, runner, cls):
      Trainer.__init__(self, runner)
      self.cls = cls

   def improve(self, state, conf, insts):
      cwd = path.join("training","iter-%03d-%s"%(state.it,conf))
      system("rm -fr %s" % cwd)
      system("mkdir -p %s" % cwd)
      init = self.runner.recall(conf)
      init = " ".join(["%s %s"%(x,init[x]) for x in sorted(init)])
      
      f_scenario = path.join(cwd, "scenario.txt")
      f_params = path.join(cwd, "params.txt")
      f_instances = path.join(cwd, "instances.txt")
      f_empty = path.join(cwd, "empty.tst")
      f_init = path.join(cwd, "init_00")
      
      file(f_scenario,"w").write(SCENARIO % (self.cls,1,3600)) # TODO
      file(f_params,"w").write(simple(self.config))
      file(f_instances,"w").write("\n".join(insts))
      file(f_empty,"w").write("")
      file(f_init,"w").write(init)

      #params = paramils.reparamils.run_reparamils(
      #   "scenario.txt",
      #   path.join(cwd,"paramils-out"),
      #   cwd,
      #   count=state.cores,
      #   N=len(insts),
      #   validN=str(len(insts)),
      #   init="init_00",
      #   #out=None,
      #   out=file(path.join(cwd,"paramils.out"),"w"),
      #   time_limit=state.train_limit)

      #params = self.runner.clean(params)
      #return self.runner.name(params) 

      return conf

