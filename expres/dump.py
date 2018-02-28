from . import details

def processed(bid, pids, results, dkey=None):
   data = details.processed(bid, pids, results)

   print "Legend:"
   out = "%25s" % "problem:"
   for (i,pid) in enumerate(pids):
      out += "%10s" % ("%02d:" % i)
      print "%02d: %s" % (i,pid)
   print
   
   print "Processed:"
   print out
   for d in sorted(data, key=dkey):
      out = "%25s" % d[0]
      for pid in pids:
         out += "%10s" % data[d][pid]
      print out
   print

