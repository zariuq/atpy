import subprocess
from subprocess import STDOUT

#PERF = "perf stat -e task-clock:up,page-faults:up,instructions:u"
PERF = ""

E_BIN = "eprover"
E_ARGS = "%s -p --resources-info --memory-limit=20480 --print-statistics --tstp-format"
E_DEFAULTS = "-s"

LIMIT = {
   "T": lambda x: "--soft-cpu-limit=%s --cpu-limit=%s" % (x,int(x)+1),
   "P": lambda x: "--processed-set-limit=%s" % x,
   "C": lambda x: "--processed-clauses-limit=%s" % x,
   "G": lambda x: "--generated-limit=%s" % x
}

#E_ARGS = "%s -s -p --free-numbers --resources-info --memory-limit=1024 --print-statistics --tstp-format --training-examples=3"
#E_ARGS = "--cpu-limit=%s -s -p --free-numbers --resources-info --memory-limit=1024 --print-statistics --tstp-format --training-examples=3"

def cmd(f_problem, proto, limit, ebinary=None, eargs=None):
   "Limit format is: 'Tnnn-Pnnn-Cnnn-Gnnn' or a subexpression, even like 'Tnnn'."
   ebinary = ebinary if ebinary else E_BIN
   if eargs and 'eargs' in eargs:
       if 'wl' in eargs:
           if 'bid-directory' in eargs and eargs['bid-directory']:
               eargs_string = "%s %s/%s/%s" % (eargs['eargs'], eargs['wl'], eargs['pid'], f_problem.split('/')[-2])
           else:
               eargs_string = "%s %s/%s" % (eargs['eargs'], eargs['wl'], eargs['pid'])
       elif 'wldir':
           eargs_string = "%s --watchlist-dir=%s" % (eargs['eargs'], eargs['wldir'])
       else:
           eargs_string = eargs['eargs']
   else:
        eargs_string = E_DEFAULTS
   
   limit = "T%s" % limit if isinstance(limit,int) else limit

   try:
      limit = [LIMIT[x[0]](x[1:]) for x in limit.split("-")]
   except:
      raise Exception("atpy.eprover.runner: Unknown E limit for eprover.runner (%s)"%limit)
   limit = " ".join(limit)

   estatic = E_ARGS % "%s %s" % (limit, eargs_string)
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

