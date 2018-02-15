import os

PROTOS_DIR = os.getenv("EXPRES_PROTOS", "./00PROTOS")

def path(pid):
   return os.path.join(PROTOS_DIR, pid)

def load(pid):
   return file(path(pid)).read().strip()

def save(pid, proto):
   file(path(pid),"w").write(proto.strip())

