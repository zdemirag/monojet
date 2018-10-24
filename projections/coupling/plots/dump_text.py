import ROOT
import sys
from array import array

#folder = "../inputs/l100_theory/"
#folder = "../inputs/l100_experiment/"
#folder = "../inputs/l100_combined/"
folder = "../inputs/l1_combined/"

couple = [1.0, 0.75, 0.5, 0.3, 0.2, 0.05, 0.01]
proc = "Vector"

for coupling_choice in couple:

#coupling_choice = 0.01
 str_coupling = str(coupling_choice).replace(".","p")
 #print str_coupling
 infile = ROOT.TFile(folder+"higgsCombine_COMB_"+str(proc)+"_gq_"+str_coupling+".root","READ")
 #print folder+"higgsCombine_COMB_"+str(proc)+"_gq_"+str_coupling+".root"
 tree   = infile.Get("limit")

 tree.GetEntry(0)
 previous = tree.mh

 i = -1
 mass = []
 exp = []
 obs = []
 coupling = []
 exp_m1 = []
 exp_m2 = []
 exp_p1 =[]
 exp_p2 = []

 for entry in tree:
     if entry.mh is "": continue
     if entry.mh != previous:
         previous = entry.mh
         i = i+1
     med = str(entry.mh)[:-6][3:]
     mdm = str(entry.mh)[4:][3:]
     if 3*float(mdm) != float(med): continue
     
     if i == 0: continue
 
     if entry.quantileExpected == -1.0:
         obs.append(float(entry.limit))

     if entry.quantileExpected == 0.5:
         mass.append(float(med))
         exp.append(float(entry.limit))
         coupling.append(coupling_choice)
         
     if "0.97" in str(entry.quantileExpected):
         exp_p2.append(entry.limit)                                                                                                                              
     if "0.83" in str(entry.quantileExpected):
         exp_p1.append(entry.limit)                                                                                                                                                         
     if "0.025" in str(entry.quantileExpected):
         exp_m2.append(entry.limit)                                                                                                                                                         
     if "0.15" in str(entry.quantileExpected):
         exp_m1.append(entry.limit)                                                                                                                                                        
      
 
 for i in range(len(mass)):
     #print exp[i], obs[i], mass[i], coupling[i], exp_m2[i], exp_m1[i], exp_p2[i], exp_p1[i]
     print exp[i], mass[i], coupling[i]
