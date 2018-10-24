import ROOT 
import sys,os 

from itertools import product

mmed = [10,20,30,40,50,60,70,80,90,100,125,150,200,300,325,400,500,525,600,725,800,925,1000,1125,1200,1325,1400,1525,1600,1725,1800,1925,2000]
mdm  = [1,5,10,15,20,25,30,35,40,45,50,60,75,80,100,125,150,175,200,225,250,275,300,300,325,350,400,500,600,700,800,900,1000,1250,1500,1750,2000]

exp  = [ '805%04d%04d'%(i,j) for i,j in product(mmed,mdm) ] 

# make a crazy string
# This string has the number for coupling, mediator mass, and darkmattermass 

stri = ",".join(exp)

dry = "--dry-run"

cmd = 'combineTool.py -M Asymptotic monojet_scalar.txt -t -1 --setParameters lumiScale=100 --freezeParameters lumiScale --cl=0.95 --rMin=-5 --rMax=5 -m %s --job-mode lxbatch --task-name "Moriond" -n CENTRAL --sub-opts "-q 1nh " --merge 2 '%(stri)

#print cmd 
os.system(cmd)
