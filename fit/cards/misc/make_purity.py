from ROOT import *

c1 = TCanvas("c1","c1")

category = "monojet"

file0 = TFile("gjets_fullhist_"+category+".root","READ")
h0_1 = file0.Get("QCD_1000To1500_met_gjets")
h0_2 = file0.Get("QCD_700To1000_met_gjets")
h0_3 = file0.Get("QCD_500To700_met_gjets")
h0_4 = file0.Get("QCD_300To500_met_gjets")

h0_1.Add(h0_2)
h0_1.Add(h0_3)
h0_1.Add(h0_4)

for i in range(1,h0_1.GetNbinsX()+1):
    content = h0_1.GetBinContent(i)
    width = h0_1.GetBinLowEdge(i+1)-h0_1.GetBinLowEdge(i)
    h0_1.SetBinContent(i,content*width)

h0_1.SetTitle("purity_"+category)
h0_1.SetName("purity_"+category)

print h0_1.Integral()

file1 = TFile("purity_"+category+".root","RECREATE")
file1.cd()
h0_1.Write()
file1.Close()

#c1.SaveAs("zvv_compare.root")


