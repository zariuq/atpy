import math

PREFIX = {
   "+": "+1",
   "-": "+10",
   "*": ""
}

BOOSTS = {
   "WRONG:POS": 1,
   "WRONG:NEG": 10
}

def count(ftrs, vector, emap, offset, strict=True):
   for ftr in ftrs:
      if ftr.startswith("$"):
         continue
      if "/" in ftr:
         parts = ftr.split("/")
         ftr = parts[0]
         inc = int(parts[1])
         if inc == 0:
            continue
      else:
         inc = 1
      if (not strict) and (ftr not in emap):
         continue
      fid = emap[ftr] + offset
      vector[fid] = vector[fid]+inc if fid in vector else inc

def proofstate(ftrs, vector, offset):
   #state = ""
   for ftr in ftrs:
      if not ftr.startswith("$"):
         continue
      (num, val) = ftr[1:].split("/")
      (num, val) = (int(num), float(val))
      if not val:
         continue
      #state += " "
      ##state += "%s:%d" % (num+offset, 1000*val)
      #state += "%s:%0.3f" % (num+offset, val)
      vector[offset+num] = val
   #return state

def string(sign, vector):
   ftrs = ["%s:%s"%(fid,vector[fid]) for fid in sorted(vector)] 
   ftrs = "%s %s"%(PREFIX[sign], " ".join(ftrs))
   return ftrs

def normalize(vector):
    non0 = len([x for x in vector if vector[x]])
    non0 = math.sqrt(non0)
    return {x:vector[x]/non0 for x in vector}

def encode(pr, emap, strict=True):
   (sign,clause,conj) = pr.strip().split("|")
   vector = {}
   count(clause.strip().split(" "), vector, emap, 0, strict)
   conjs = conj.strip().split(" ")
   count(conjs, vector, emap, len(emap), strict)
   proofstate(conjs, vector, 2*len(emap))
   #vector = normalize(vector)
   return string(sign, vector)

def make(pre, emap, out=None, strict=True):
   train = []
   for pr in pre:
      tr = encode(pr, emap, strict)
      if out:
         out.write(tr)
         out.write("\n")
      else:
         train.append(tr)
   return train if not out else None

def boost(f_in, f_out, out, method="WRONG:POS"):
   if method not in BOOSTS:
      raise Exception("Unknown boost method (%s)")
   CLS = BOOSTS[method]

   ins = file(f_in).read().strip().split("\n")
   outs = file(f_out).read().strip().split("\n")

   for (correct,predicted) in zip(ins,outs):
      out.write(correct)
      out.write("\n")
      cls = int(correct.split()[0])
      if cls == CLS and cls != int(predicted):
         out.write(correct)
         out.write("\n")

