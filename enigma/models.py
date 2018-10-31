import os
from . import enigmap, pretrains, trains, liblinear, protos, xgbooster
from .. import expres

ENIGMA_ROOT = os.getenv("ENIGMA_ROOT", "./Enigma")

def path(name, filename=None):
   if filename:
      return os.path.join(ENIGMA_ROOT, name, filename)
   else:
      return os.path.join(ENIGMA_ROOT, name)

def collect(name, rkeys, version):
   f_pre = path(name, "train.pre")
   pretrains.prepare(rkeys, version)
   pretrains.make(rkeys, out=file(f_pre, "w"))

def setup(name, rkeys, version):
   os.system("mkdir -p %s" % path(name))
   if rkeys:
      collect(name, rkeys, version)

   f_pre = path(name, "train.pre")
   f_map = path(name, "enigma.map")
   f_log = path(name, "train.log")
   if os.path.isfile(f_log):
      os.system("rm -f %s" % f_log)

   emap = enigmap.create(file(f_pre))
   enigmap.save(emap, f_map, version)
   return emap

def standard(name, rkeys=None, version="VHSLC", force=False, gzip=True):
   f_pre = path(name, "train.pre")
   f_in  = path(name, "train.in")
   f_mod = path(name, "model.lin")
   f_out = path(name, "train.out")
   f_log = path(name, "train.log")

   if not force and os.path.isfile(f_mod):
      return

   emap = setup(name, rkeys, version)
   if not emap:
      os.system("rm -fr %s" % path(name))
      return False

   trains.make(file(f_pre), emap, out=file(f_in, "w"))
   print "training", name
   liblinear.train(f_in, f_mod, f_out, f_log)
      
   stat = liblinear.stats(f_in, f_out)
   print "\n".join(["%s = %s"%(x,stat[x]) for x in sorted(stat)])

   if gzip:
      os.system("cd %s; gzip *.pre *.in *.out" % path(name))

   return True

def smartboost(name, rkeys=None, version="VHSLC", force=False, gzip=True, xgb=False):
   it = 0
   f_pre = path(name, "train.pre")
   f_log = path(name, "train.log")
   f_in  = path(name, "%02dtrain.in" % it)
   f_Mod = path(name, "model.lin")
   if not force and os.path.isfile(f_Mod):
      return
  
   emap = setup(name, rkeys, version)
   if not emap:
      os.system("rm -fr %s" % path(name))
      return False
   trains.make(file(f_pre), emap, out=file(f_in, "w"))

   method = None
   print "smart-boosting", name
   log = file(f_log, "a")
   while True:
      log.write("\n--- ITER %d ---\n\n" % it)
      f_in  = path(name, "%02dtrain.in" % it)
      f_in2 = path(name, "%02dtrain.in" % (it+1))
      f_out = path(name, "%02dtrain.out" % it)
      f_mod = path(name, "%02dmodel.lin" % it)
      log.flush()
      liblinear.train(f_in, f_mod, f_out, f_log)
      stat = liblinear.stats(f_in, f_out)
      log.write("\n".join(["%s = %s"%(x,stat[x]) for x in sorted(stat)]))
      log.write("\n")

      if not method:
         if stat["ACC:POS"] < stat["ACC:NEG"]:
            method = "WRONG:POS"
            terminate = lambda s: s["ACC:POS"] >= s["ACC:NEG"]
         else:
            method = "WRONG:NEG"
            terminate = lambda s: s["ACC:NEG"] >= s["ACC:POS"]

      #if stat["ACC:POS"] >= stat["ACC:NEG"]:
      #if stat["WRONG:POS"] == 0:
      if terminate(stat):
         os.system("cp %s %s" % (f_mod, f_Mod))
         break
      trains.boost(f_in, f_out, out=file(f_in2,"w"), method=method)
      it += 1

   stat = liblinear.stats(f_in, f_out)
   print "\n".join(["%s = %s"%(x,stat[x]) for x in sorted(stat)])
   
   if xgb:
      f_xgb = path(name, "model.xgb")
      xgbooster.train(f_in, f_xgb, log)
   log.close()
      
   if gzip:
      os.system("cd %s; gzip *.pre *.in *.out" % path(name))
   
   return True

def loop(model, pids, results=None, bid=None, limit=None, nick=None, xgb=False, efun="Enigma",
         cores=4, version="VHSLC", force=False, gzip=True, eargs="", update=False):

   if results is None:
      results = {}
   if update:
      results.update(expres.benchmarks.eval(bid, pids, limit, cores=cores, eargs=eargs))
   if nick:
      model = "%s/%s" % (model, nick)
   
   smartboost(model, results, version, force=force, gzip=gzip, xgb=xgb)
   new = [
      protos.standalone(pids[0], model, mult=0, noinit=True, efun=efun),
      protos.combined(pids[0], model, mult=0, noinit=True, efun=efun)
   ]
   if update:
      pids.extend(new)
      results.update(expres.benchmarks.eval(bid, new, limit, cores=cores, eargs=eargs))
   return new



def join(name, models, combine=max):
   f_maps = [path(model, "enigma.map") for model in models]
   emap = enigmap.join(f_maps)

   ws1 = {ftr:[] for ftr in emap}
   ws2 = {ftr:[] for ftr in emap}
   for model in models:
      f_mod = path(model, "model.lin")
      f_map = path(model, "enigma.map")
      (header,w1,w2) = liblinear.load(f_mod, f_map)
      for ftr in w1:
         if w1[ftr] != 0:
            ws1[ftr].append(w1[ftr])
      for ftr in w2:
         if w2[ftr] != 0:
            ws2[ftr].append(w2[ftr])
   
   w1 = {ftr:combine(ws1[ftr]) for ftr in emap if ws1[ftr]}
   w2 = {ftr:combine(ws2[ftr]) for ftr in emap if ws2[ftr]}

   os.system("mkdir -p %s" % path(name))
   f_mod = path(name, "model.lin")
   f_map = path(name, "enigma.map")
   enigmap.save(emap, f_map)
   liblinear.save(header, w1, w2, emap, f_mod)

