import re

STATUS_OK = ['Satisfiable', 'Unsatisfiable', 'Theorem', 'CounterSatisfiable']
STATUS_OUT = ['ResourceOut', 'GaveUp']
STATUS_ALL = STATUS_OK + STATUS_OUT

PATS = {
   "RUNTIME":   re.compile(r"^\s*(\d*\.\d*)\s*task-clock:up"),
   "MILINS":    re.compile(r"^\s*([0-9,]*)\s*instructions:up"),
   "STATUS":    re.compile(r"^# SZS status (\S*)"),
   "PROCESSED": re.compile(r"^# Processed clauses\s*: (\S*)"),
   "GENERATED": re.compile(r"^# Generated clauses\s*: (\S*)"),
   "PROOFLEN":  re.compile(r"^# Proof object total steps\s*: (\S*)"),
   "PRUNED":    re.compile(r"^# Removed by relevancy pruning/SinE\s*: (\S*)")
}

def value(strval):
   if strval.isdigit():
      return int(strval)
   if strval.find(".") >= 0:
      try:
         return float(strval)
      except:
         pass
   return strval

def parse(f_out, trains=False):
   result = {}
   result["STATUS"] = "Unknown"
   if trains:
      result["POS"] = []
      result["NEG"] = []

   for line in file(f_out):
      line = line.rstrip()
      if line and (line[0] == "#" or line[0] == " "):
         for pat in PATS:
            mo = PATS[pat].search(line)
            if mo:
               result[pat] = value(mo.group(1))
      if trains and line.startswith("cnf(") and \
         ("$false" not in line) and ("epred" not in line):
         if "trainpos" in line:
            result["POS"].append(line)
         elif "trainneg" in line:
            result["NEG"].append(line)

   if "RUNTIME" in result:
      result["RUNTIME"] /= 1000.0
   if "MILINS" in result:
      result["MILINS"] = int(result["MILINS"].replace(",",""))/(10**6)
   return result

def solved(result, limit=None):
   ok = "STATUS" in result and result["STATUS"] in STATUS_OK
   if limit:
      return ok and result["RUNTIME"] <= limit
   return ok

def error(result):
   return "STATUS" not in result or result["STATUS"] not in STATUS_ALL

