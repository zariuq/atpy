#!/usr/bin/python

import sys
import os
from atpy import enigma

def predict(name, f_cnfs, f_conj):
   os.system("rm -fr predict.pre predict.in predict.out")
   emap = enigma.enigmap.load(enigma.models.path(name, "enigma.map"))
   enigma.pretrains.translate(f_cnfs, f_conj, "predict.pre")
   pre = file("predict.pre").read().strip().split("\n")
   enigma.trains.make(pre, emap, file("predict.in","w"))
   enigma.liblinear.predict("predict.in", enigma.models.path(name, "model.lin"), "predict.out", "/dev/null")

   preds = file("predict.out").read().strip().split("\n")
   for line in file(f_cnfs):
      line = line.strip()
      if preds:
         print "%s %s" % (preds.pop(0), line)
      elif line:
         raise Exception("Classificator mismatch (too many clauses)")
   if preds:
      raise Exception("Classificator mismatch (too many predictions)")
   os.system("rm -fr predict.pre predict.in predict.out")

if len(sys.argv) != 4:
   print "usage: %s model-name classify.cnfs conjecture.cnfs" % os.path.basename(sys.argv[0])
else:
   predict(sys.argv[1], sys.argv[2], sys.argv[3])



