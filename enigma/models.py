import os
from . import enigmap, pretrains, trains, liblinear

ENIGMA_ROOT = os.getenv("ENIGMA_ROOT", "./Enigma")

def path(name, filename=None):
   if filename:
      return os.path.join(ENIGMA_ROOT, name, filename)
   else:
      return os.path.join(ENIGMA_ROOT, name)

def collect(name, rkeys):
   f_pre = path(name, "train.pre")
   os.system("mkdir -p %s" % path(name))
   pretrains.prepare(rkeys)
   pretrains.make(rkeys, out=file(f_pre, "w"))

def setup(name, rkeys):
   if rkeys:
      collect(name, rkeys)

   f_pre = path(name, "train.pre")
   f_map = path(name, "enigma.map")
   f_log = path(name, "train.log")
   if os.path.isfile(f_log):
      os.system("rm -f %s" % f_log)

   emap = enigmap.create(file(f_pre))
   enigmap.save(emap, f_map)
   return emap

def standard(name, rkeys=None):
   f_pre = path(name, "train.pre")
   f_in  = path(name, "train.in")
   f_mod = path(name, "model.lin")
   f_out = path(name, "train.out")
   f_log = path(name, "train.log")

   emap = setup(name, rkeys)
   trains.make(file(f_pre), emap, out=file(f_in, "w"))
   liblinear.train(f_in, f_mod, f_out, f_log)

def smartboost(name, pre):
   pass

def join(name, models):
   pass

aim01

aim01---name0
aim01---nameS

aim01---aim-train--1s--singles--xProblem.p0

aim01--aim-train+1s+singles+xProblem.p+standardS--aim-train+1s+union+standard

pid--name--0

name ::= bid/pid--1s/singles/problem.p/standardS





