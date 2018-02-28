import os
import json
from . import details

HTML_DIR = os.getenv("EXPRES_HTML", 
   os.path.join(os.getenv("HOME"),"public_html","expres"))

def path(f_name):
   return os.path.join(HTML_DIR, f_name)

def begin(out, title, data, exp):
   out.write(
'''<html>
<head>
   <title>%s</title>
   <link rel="stylesheet" type="text/css" href="../static/style.css">
   <script src="../static/sortable.js"></script>
   <script src="data/%s.js"></script>
   <script>
   window.onload = function() {
      updateLegend(%s, "legend___%s");
      updateTable(%s, "%s", 0, 1);
   };
   </script>
</head>
<body>
<h1>%s</h1>
<p>experiment id: %s
<br>data id: %s
''' % (title, data, data, data, data, data, title, exp, data))

def table(out, data):
   out.write(
'''
<h2>Legend</h2>

<div class="tables">
<div class="box">
   <table id="legend___%s"></table>
</div>
</div>

<h2>Details</h2>
<div class="tables">
<div class="box">
   <table id="%s"></table>
</div>
</div>
''' % (data, data))

def end(out):
   out.write( 
'''
</body>
</html>
''')
   out.close()

def processed(bid, pids, results, exp="results", data="data"): 
   proc = details.processed(bid, pids, results)
   f_out = path(os.path.join(exp, data+".html"))
   os.system("mkdir -p %s" % os.path.dirname(f_out))
   out = file(f_out, "w")
  
   begin(out, "Processed @ %s" % bid, data, exp)
   table(out, data)
   end(out)

   legend = dict(enumerate(pids))

   f_js = path(os.path.join(exp, "data", data+".js"))
   os.system("mkdir -p %s" % os.path.dirname(f_js))
   js = {}
   js["HEADER"] = ["problem"]+legend.keys()
   js["CLASSES"] = {}
   js["DATA"] = [[d[0]]+[proc[d][pid] for pid in pids] for d in sorted(proc)]
   js["LEGEND"] = legend
   file(f_js,"w").write("var %s = %s;" % (data,json.dumps(js)))

