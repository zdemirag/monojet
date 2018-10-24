import ROOT 
import sys,os 

from itertools import product
exp = ['80000300010','80000600020','80001500050','80002250075','80003000100','80006000200','80007500250','80012000400','80015000500','80018000600','80030001000']

# make a crazy string
# This string has the number for coupling, mediator mass, and darkmattermass 

stri = ",".join(exp)

dry = "--dry-run"

cmd = 'combineTool.py -M Asymptotic monojet_vector.txt -t -1 --freezeNuisanceGroups experiment --setParameters lumiScale=100 --freezeParameters lumiScale --cl=0.95 --rMin=-5 --rMax=5 -m %s --job-mode lxbatch --task-name "Moriond" -n CENTRAL --sub-opts "-q 1nh " --merge 2 '%(stri)

#print cmd 
os.system(cmd)
