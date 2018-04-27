from . import details, summary

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

def solved(bid, pids, results, ref=None):
   print
   print "Summary @ %s:" % bid
   data = summary.make(bid, pids, results, ref=ref) 
   for pid in sorted(data, key=lambda p: data[p][2], reverse=True):
      s = data[pid]
      if ref:
         print "%s %4s/%4s   +%2s/-%2s: %s" % ("!" if s[1] else "",s[2],s[0],s[3],s[4],pid)
      else:
         print "%s %4s/%4s: %s" % ("!" if s[1] else "",s[2],s[0],pid)
   print

