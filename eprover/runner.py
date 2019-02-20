import subprocess
from subprocess import STDOUT

#PERF = "perf stat -e task-clock:up,page-faults:up,instructions:u"
PERF = ""

E_BIN = "eprover"
E_ARGS = "%s -p --resources-info --memory-limit=20480 --print-statistics --tstp-format"
E_DEFAULTS = "-s"

#E_ARGS = "%s -s -p --free-numbers --resources-info --memory-limit=1024 --print-statistics --tstp-format --training-examples=3"
#E_ARGS = "--cpu-limit=%s -s -p --free-numbers --resources-info --memory-limit=1024 --print-statistics --tstp-format --training-examples=3"

def cmd(f_problem, proto, limit, ebinary=None, eargs=None):
   ebinary = ebinary if ebinary else E_BIN
   eargs = eargs if eargs else E_DEFAULTS
   if isinstance(limit, int):
      limit = "--soft-cpu-limit=%s --cpu-limit=%s" % (limit, limit+1)
   elif isinstance(limit, str) and "-" in limit:
      # otherwise limit format "Txxx-Cyyy"
      (t,p) = limit.split("-")
      (t,p) = (t[1:], p[1:])
      (t,p) = (int(t), int(p))
      limit = "--soft-cpu-limit=%s --cpu-limit=%s --processed-set-limit=%s" % (t,t+1,p)
   else:
      raise Exception("atpy.eprover.runner: Unknown E limit for eprover.runner (%s)"%limit)

   estatic = E_ARGS % "%s %s" % (limit, eargs)
   return "%s %s %s %s %s" % (PERF,ebinary,estatic,proto,f_problem)

def run(f_problem, proto, limit, f_out=None, ebinary=None, eargs=None):
   cmd0 = cmd(f_problem, proto, limit, ebinary, eargs)
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

