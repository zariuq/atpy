from multiprocessing import Pool
import os

from .. import eprover
from . import protos, results, solved

BENCHMARKS_DIR = os.getenv("EXPRES_BENCHMARKS", 
   os.path.join(os.getenv("HOME"),"projects","atp","benchmarks"))

def path(bid, problem):
   return os.path.join(BENCHMARKS_DIR, bid, problem)

def problems(bid):
   probs = os.listdir(os.path.join(BENCHMARKS_DIR, bid))
   probs = [x for x in probs if os.path.isfile(os.path.join(BENCHMARKS_DIR, bid, x)) and not x.endswith(".cnf")]
   return probs

def compute(bid, pid, problem, limit):
   f_problem = path(bid, problem)
   proto = protos.load(pid)
   f_out = results.path(bid, pid, problem, limit)
   os.system("mkdir -p %s" % os.path.dirname(f_out))
   out = eprover.runner.run(f_problem, proto, limit, f_out)
   return results.load(bid, pid, problem, limit)

def runjob(job):
   return compute(job[0], job[1], job[2], job[3])

def eval(bid, pids, limit, cores=4):
   probs = problems(bid)
   jobs = [(bid,pid,problem,limit) for pid in pids for problem in probs]
   pool = Pool(cores)
   res = pool.map(runjob, jobs)
   res = dict(zip(jobs, res))
   solved.update(res)
   return res

