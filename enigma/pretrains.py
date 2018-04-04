import subprocess
from .. import expres, eprover
import os

def prepare(rkeys):
   for (bid, pid, problem, limit) in rkeys:

      f_problem = expres.benchmarks.path(bid, problem)
      f_cnf = f_problem+".cnf"
      if not os.path.isfile(f_cnf):
         file(f_cnf, "w").write(eprover.runner.cnf(f_problem))

      result = None
      #result = rkeys[(bid,pid,problem,limit)]
      f_pos = expres.results.path(bid, pid, problem, limit, ext="pos")
      f_neg = expres.results.path(bid, pid, problem, limit, ext="neg")
      if not (os.path.isfile(f_pos) and os.path.isfile(f_neg)):
         result = expres.results.load(bid, pid, problem, limit, trains=True)
         if not os.path.isfile(f_pos):
            file(f_pos, "w").write("\n".join(result["POS"]))
         if not os.path.isfile(f_neg):
            file(f_neg, "w").write("\n".join(result["NEG"]))
      
      f_pre = expres.results.path(bid, pid, problem, limit, ext="pre")
      if not os.path.isfile(f_pre):
         out = file(f_pre, "w")
         subprocess.call(["enigma-features", "--free-numbers", f_pos, f_neg, f_cnf], \
            stdout=out)
            #stdout=out, stderr=subprocess.STDOUT)
         out.close()

def make(rkeys, out=None):
   pre = []
   for (bid, pid, problem, limit) in rkeys:
      f_pre = expres.results.path(bid, pid, problem, limit, ext="pre")
      if out:
         tmp = file(f_pre).read().strip()
         if tmp:
            out.write(tmp)
            out.write("\n")
      else:
         pre.extend(file(f_pre).read().strip().split("\n"))
   return pre if not out else None

