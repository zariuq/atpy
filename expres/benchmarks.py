from multiprocessing import Pool
import os

from .. import eprover
from . import protos, results
from . import solved as solvedb

BENCHMARKS_DIR = os.getenv("EXPRES_BENCHMARKS", 
   os.path.join(os.getenv("HOME"),"projects","atp","benchmarks"))

def path(bid, problem):
   return os.path.join(BENCHMARKS_DIR, bid, problem)

def problems(bid):
   probs = os.listdir(os.path.join(BENCHMARKS_DIR, bid))
   probs = [x for x in probs if os.path.isfile(os.path.join(BENCHMARKS_DIR, bid, x)) and not x.endswith(".cnf")]
   return probs

def compute(bid, pid, problem, limit, force=False):
   f_problem = path(bid, problem)
   proto = protos.load(pid)
   f_out = results.path(bid, pid, problem, limit)
   if force or not os.path.isfile(f_out):
      os.system("mkdir -p %s" % os.path.dirname(f_out))
      out = eprover.runner.run(f_problem, proto, limit, f_out)
   return results.load(bid, pid, problem, limit)

def runjob(job):
   return compute(job[0], job[1], job[2], job[3])

def runjob_force(job):
   return compute(job[0], job[1], job[2], job[3], force=True)

def eval(bid, pids, limit, cores=4, force=False):
   probs = problems(bid)
   if isinstance(limit, int):
      eta = "ETA %ds" % (float(len(pids))*len(probs)*limit/cores)
   else:
      eta = "%d jobs/cpu" % (float(len(pids))*len(probs)/cores)
   print "Evaluating %s protos @ %s (%d) @ limit %s @ %s cores: %s" % (len(pids), bid, len(probs), limit, cores, eta)
   jobs = [(bid,pid,problem,limit) for pid in pids for problem in probs]
   pool = Pool(cores)
   res = pool.map_async(runjob if not force else runjob_force, jobs).get(365*24*3600)
   res = dict(zip(jobs, res))
   solvedb.update(res)
   pool.close()
   return res

def solved(bid, pids, limit, cores=4, force=False):
   res = eval(bid, pids, limit, cores=cores, force=force)
   res = {x:res[x] for x in res if eprover.result.solved(res[x])}
   return res

def get(bid, pids, limit):
   probs = problems(bid)
   rkeys = [(bid,pid,problem,limit) for pid in pids for problem in probs]
   print "Loading %d results ..." % len(rkeys)
   ret = {rkey:results.load(*rkey) for rkey in rkeys if results.exists(*rkey)}
   print "done."
   return ret

