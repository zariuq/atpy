import os

def load(f_map):
   emap = {}
   if not os.path.exists(f_map):
      return emap
   for line in file(f_map):
      if line.startswith("version"):
         continue
      (fid,ftr) = line.strip().split("(")[1].split(",")
      fid = int(fid.strip(", "))
      ftr = ftr.strip('") .')
      emap[ftr] = fid
   return emap

def save(emap, f_map, version):
   rev = {emap[ftr]:ftr for ftr in emap}
   out = file(f_map, "w")
   out.write('version("%s").\n' % version)
   for x in sorted(rev):
      out.write('feature(%s, "%s").\n' % (x,rev[x]))
   out.close()

def create(pre):

   def add(features, new):
      for feature in new.strip().split(" "):
         if not feature:
            continue
         if "/" in feature:
            feature = feature.split("/")[0]
         features.add(feature)

   features = set()
   for pr in pre:
      (sign,clause,conj) = pr.strip().split("|")
      add(features, clause)
      add(features, conj)
   return {y:x for (x,y) in enumerate(sorted(features), start=1)}

def join(f_maps):
   features = set()
   for f_map in f_maps:
      features.update(load(f_map).keys())
   return {y:x for (x,y) in enumerate(sorted(features), start=1)}

