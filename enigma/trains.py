
PREFIX = {
   "+": "+1",
   "-": "+10",
   "*": "Should not ever see me"
}

def count(ftrs, counts, emap, offset):
   for ftr in ftrs:
      if "/" in ftr:
         parts = ftr.split("/")
         ftr = parts[0]
         inc = int(parts[1])
         if inc == 0:
            continue
      else:
         inc = 1
      fid = emap[ftr] + offset
      counts[fid] = counts[fid]+inc if fid in counts else inc

def encode(pr, emap):
   (sign,clause,conj) = pr.strip().split("|")
   counts = {}
   count(clause.strip().split(" "), counts, emap, 0)
   count(  conj.strip().split(" "), counts, emap, len(emap))
   ftrs = ["%s:%s"%(fid,counts[fid]) for fid in sorted(counts)] 
   ftrs = "%s %s"%(PREFIX[sign], " ".join(ftrs))
   return ftrs

def make(pre, emap, out=None):
   train = []
   for pr in pre:
      tr = encode(pr, emap)
      if out:
         out.write(tr)
         out.write("\n")
      else:
         train.append(tr)
   return train if not out else None

def boost(f_in, f_out, out, method="WRONG:POS"):
   if method != "WRONG:POS":
      raise Exception("Unknown boost method")

   ins = file(f_in).read().strip().split("\n")
   outs = file(f_out).read().strip().split("\n")

   for (correct,predicted) in zip(ins,outs):
      out.write(correct)
      out.write("\n")
      cls = int(correct.split()[0])
      if cls == 1 and cls != int(predicted):
         out.write(correct)
         out.write("\n")

