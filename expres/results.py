import os
from .. import eprover

RESULTS_DIR = os.getenv("EXPRES_RESULTS", "./00RESULTS")

def path(bid, pid, problem, limit, pidkey="", ext="out"):
   d_pid = "%s%s/%s%s" % (limit, "s" if isinstance(limit,int) else "", pidkey, pid)
   f_out = "%s.%s" % (problem, ext)
   return os.path.join(RESULTS_DIR, bid, d_pid, f_out)

def output(bid, pid, problem, limit, pidkey=""):
   return file(path(bid, pid, problem, limit, pidkey)).read()

def exists(bid, pid, problem, limit, pidkey="", ext="out"):
   return os.path.isfile(path(bid, pid, problem, limit, pidkey, ext=ext))

def save(bid, pid, problem, limit, out, pidkey=""):
   f_out = path(bid, pid, problem, limit, pidkey)
   os.system("mkdir -p %s" % os.path.dirname(f_out))
   file(f_out,"w").write(out)

def load(bid, pid, problem, limit, pidkey="", trains=False):
   f_out = path(bid, pid, problem, limit, pidkey)
   return eprover.result.parse(f_out, trains=trains)

