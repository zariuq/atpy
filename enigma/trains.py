
PREFIX = {
   "+": "+1",
   "-": "+10",
   "*": "Should not ever see me"
}

def count(ftrs, counts, emap, offset):
   for ftr in ftrs:
      fid = emap[ftr] + offset
      counts[fid] = counts[fid]+1 if fid in counts else 1

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

