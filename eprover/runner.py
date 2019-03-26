import subprocess
from subprocess import STDOUT

#PERF = "perf stat -e task-clock:up,page-faults:up,instructions:up"
PERF = ""

#E_BIN = "eprover"
E_BIN = "/home/zar/bin/tbin/eprover"
E_ARGS = "%s -s -p --resources-info --memory-limit=1024 --print-statistics --tstp-format --free-numbers "
#E_ARGS = "%s -s -p --free-numbers --resources-info --memory-limit=1024 --print-statistics --tstp-format --training-examples=3"
#E_ARGS = "--cpu-limit=%s -s -p --free-numbers --resources-info --memory-limit=1024 --print-statistics --tstp-format --training-examples=3"

def cmd(f_problem, proto, limit, watchlist_dir=None):
   if isinstance(limit, int):
      limit = "--soft-cpu-limit=%s --cpu-limit=%s" % (limit,limit+1)
   elif isinstance(limit, str) and "+" in limit:
      # limit format "Txxx+Cyyy"
      (t,p) = limit.split("+")
      (t,p) = (t[1:], p[1:])
      (t,p) = (int(t), int(p))
      limit = "--soft-cpu-limit=%s --cpu-limit=%s --processed-clauses-limit=%s" % (t,t+1,p)
   elif isinstance(limit, str) and 'C' == limit[0]:
      # limit format "Cyyy" (seriously, regex would be more appropriate)
      limit = "--processed-clauses-limit=%s" % (int(limit[1:]))
   else:
      raise Exception("Grackle: Unknown E limit for eprover.runner (%s)"%limit)

   eargs = E_ARGS % limit
   if watchlist_dir:
       if watchlist_dir[0] == 1:
           return "%s %s %s %s %s %s" % (PERF,E_BIN,eargs,watchlist_dir[1],proto,f_problem)
       if watchlist_dir[0] == 2: # What a cheap hack
           problem_name = f_problem.split('/')[-1]
           return "%s %s %s %s/%s %s %s" % (PERF,E_BIN,eargs,watchlist_dir[1],problem_name,proto,f_problem)
   else:
       return "%s %s %s %s %s" % (PERF,E_BIN,eargs,proto,f_problem)

def run(f_problem, proto, limit, watchlist_dir, f_out=None):
   cmd0 = cmd(f_problem, proto, limit, watchlist_dir)
   if f_out:
      out = file(f_out,"w")
      subprocess.call(cmd0, shell=True, stdout=out, stderr=STDOUT)
      out.close()
      return True
   else:
      return subprocess.check_output(cmd0, shell=True, stderr=STDOUT)

def cnf(f_problem):
   cmd0 = "%s --tstp-format --free-numbers --cnf %s" % (E_BIN,f_problem)
   return subprocess.check_output(cmd0, shell=True, stderr=STDOUT)

