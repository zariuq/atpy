import os
import json

def save(f_js, var, header, classes, rows, leg=None):
   os.system("mkdir -p %s" % os.path.dirname(f_js))
   js = {}
   js["HEADER"] = header
   js["CLASSES"] = classes
   js["DATA"] = rows
   if leg:
      js["LEGEND"] = leg
   file(f_js,"w").write("var %s = %s;" % (var,json.dumps(js)))

