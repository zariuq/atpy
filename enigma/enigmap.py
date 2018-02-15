
def load(f_map):
   nums = {}
   if not os.path.exists(f_map):
      return nums
   for line in file(f_map):
      (fid,ftr) = line.strip().split("(")[1].split(",")
      fid = int(fid.strip(", "))
      ftr = ftr.strip('") .')
      nums[ftr] = fid
   return nums

def save(emap, f_map):
   rev = {emap[ftr]:ftr for ftr in emap}
   out = file(f_map, "w")
   for x in sorted(rev):
      out.write('feature(%s, "%s").\n' % (x,rev[x]))
   out.close()

def create(pre):
   features = set()
   for pr in pre:
      (sign,clause,conj) = pr.strip().split("|")
      for feature in clause.strip().split(" "):
         features.add(feature)
      for feature in conj.strip().split(" "):
         features.add(feature)
   return {y:x for (x,y) in enumerate(sorted(features), start=1)}

def update(this, other):
   pass

