import subprocess
from subprocess import STDOUT

PERF = "perf stat -e task-clock:up,page-faults:up,instructions:up"

E_BIN = "eprover"
E_ARGS = "%s -s -p --free-numbers --resources-info --memory-limit=1024 --print-statistics --tstp-format --training-examples=3"
#E_ARGS = "--cpu-limit=%s -s -p --free-numbers --resources-info --memory-limit=1024 --print-statistics --tstp-format --training-examples=3"

def run(f_problem, proto, limit, f_out=None):
   if isinstance(limit, int):
      limit = "--cpu-limit=%s" % limit
   else:
      # otherwise limit format "Txxx+Cyyy"
      (t,p) = limit.split("+")
      (t,p) = (t[1:], p[1:])
      (t,p) = (int(t), int(p))
      limit = "--cpu-limit=%s --processed-clauses-limit=%s" % (t,p)
   eargs = E_ARGS % limit

   cmd = "%s %s %s %s %s" % (PERF,E_BIN,eargs,proto,f_problem)
   if f_out:
      out = file(f_out,"w")
      subprocess.call(cmd, shell=True, stdout=out, stderr=STDOUT)
      out.close()
      return True
   else:
      return subprocess.check_output(cmd, shell=True, stderr=STDOUT)

def cnf(f_problem):
   cmd = "%s --tstp-format --free-numbers --cnf %s" % (E_BIN,f_problem)
   return subprocess.check_output(cmd, shell=True, stderr=STDOUT)

