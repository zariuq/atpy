
PARAMS = """
   tord {Auto,LPO4,KBO6} [LPO4]
   sel {SelectMaxLComplexAvoidPosPred,SelectNewComplexAHP,SelectComplexG,SelectCQPrecWNTNp} [SelectMaxLComplexAvoidPosPred]
   prord {arity,invfreq,invfreqconstmin} [invfreqconstmin]
   simparamod {none,normal,oriented} [normal]
   srd {0,1} [0]
   forwardcntxtsr {0,1} [1]
   splaggr {0,1} [1]
   splcl {0,4,7} [4]
   sineL {10,20,40,60,80,100,500,20000} [100]
   sineR {UU,01,02,03,04} [UU]
   sinegf {1.1,1.2,1.4,1.5,2.0,5.0,6.0} [1.2]
   sineh  {hypos,none} [hypos]
   sine {0,1} [0]
"""

CONDITIONS = """
   sineL  | sine in {1}
   sineR  | sine in {1}
   sinegf | sine in {1}
   sineh  | sine in {1}
"""

FORBIDDENS = ""

def cefs_params(config):
   pars = ""
   slots = ",".join(map(str, range(config["min_slots"], config["max_slots"]+1)))
   pars += "   slots {%s} [%s]\n" % (slots, config["min_slots"])
   return pars

def simple(config):
   return PARAMS + cefs_params(config) + CONDITIONS + FORBIDDENS

