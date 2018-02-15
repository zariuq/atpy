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

def stats(f_in, f_out):
   ins = file(f_in).read().strip().split("\n")
   ins = [x.split()[0] for x in ins]
   ins = map(int, ins)

   outs = file(f_out).read().strip().split("\n")
   outs = map(int, outs)

   stat = {}
   stat["COUNT"] = 0
   stat["RIGHT"] = 0
   stat["WRONG"] = 0
   stat["POS-COUNT"] = 0
   stat["POS-RIGHT"] = 0
   stat["POS-WRONG"] = 0
   stat["NEG-COUNT"] = 0
   stat["NEG-RIGHT"] = 0
   stat["NEG-WRONG"] = 0

   for (correct,predicted) in zip(ins, outs):
      stat["COUNT"] += 1
      if correct == 1:
         stat["POS-COUNT"] += 1
      else:
         stat["NEG-COUNT"] += 1

      if correct == predicted:
         stat["RIGHT"] += 1
         if correct == 1:
            stat["POS-RIGHT"] += 1
         else:
            stat["NEG-RIGHT"] += 1
      else:
         stat["WRONG"] += 1
         if correct == 1:
            stat["POS-WRONG"] += 1
         else:
            stat["NEG-WRONG"] += 1
   
   stat["ACC"] = stat["RIGHT"] / float(stat["COUNT"])
   stat["POS-ACC"] = stat["POS-RIGHT"] / float(stat["POS-COUNT"])
   stat["NEG-ACC"] = stat["NEG-RIGHT"] / float(stat["NEG-COUNT"])

   return stat


