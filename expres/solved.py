import os
from .. import eprover

SOLVED_DIR = os.getenv("EXPRES_SOLVED", "./00SOLVED")

def path(bid, pid, limit, pidkey=""):
   f_pid = "%s%s/%s%s" % (limit, "s" if isinstance(limit,int) else "", pidkey, pid)
   return os.path.join(SOLVED_DIR, bid, f_pid)

def load(bid, pid, limit, pidkey=""):
   f_solved = path(bid, pid, limit, pidkey)
   if os.path.isfile(f_solved):
      return set(file(path(bid, pid, limit, pidkey)).read().strip().split("\n"))
   else:
      return set()

def save(bid, pid, limit, problems, pidkey=""):
   f_solved = path(bid, pid, limit, pidkey)
   os.system("mkdir -p %s" % os.path.dirname(f_solved))
   file(f_solved, "w").write(("\n".join(sorted(problems)))+"\n")

def update(results, pidkey=""):
   solved = {}
   for rkey in results:
      (bid, pid, problem, limit) = rkey[:4]
      if eprover.result.solved(results[rkey]):
         skey = (bid, pid, limit)
         if skey not in solved:
            solved[skey] = load(bid, pid, limit, pidkey)
         solved[skey].add(problem)
   for skey in solved:
      (bid, pid, limit) = skey
      save(bid, pid, limit, solved[skey], pidkey)

