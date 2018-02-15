import subprocess

PERF = ["perf", "stat", "-e", "task-clock:up,page-faults:up,instructions:up"]

def train(f_in, f_mod, f_out=None, f_log=None):
   if f_log:
      subprocess.call(PERF+["train", "-s" , "2", f_in, f_mod], \
         stdout=file(f_log, "a"), stderr=subprocess.STDOUT)
   else:
      subprocess.call(["train", "-s" , "2", f_in, f_mod])

   if f_out:
      predict(f_in, f_mod, f_out, f_log)
      

def predict(f_in, f_mod, f_out, f_log):
   if f_log:
      subprocess.call(PERF+["predict", f_in, f_mod, f_out], \
         stdout=file(f_log, "a"), stderr=subprocess.STDOUT)
   else:
      subprocess.call(["predict", f_in, f_mod, f_out])

