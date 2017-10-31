#! /usr/bin/env python                                                                                                                                                              
from ROOT import *
from array import array
#from tdrStyle import *
import math
#from pretty import plot_cms
#setTDRStyle()

def makevariations():

  #bins = [200., 230., 260.0, 290.0, 320.0, 350.0, 390.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1249.0]  
  bins = [230., 260.0, 290.0, 320.0, 350.0, 390.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1249.0]  
  bins_monov = [250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 750, 1000.0]
  
  infile = TFile("/afs/cern.ch/user/r/rgerosa/public/xZeynep/theoryUncertainties_new/theory_unc_ZW.root","READ")
  f_out = TFile("wz_unc_v3.root","recreate")

  h_orig = {}
  h = {}
  hv_orig = {}
  hv = {}
  i = 0

  samplehistos = infile.GetListOfKeys()
  for s in samplehistos: 
    obj = s.ReadObj()
    if type(obj)!=type(TH1F()): continue
    samplehist = obj
    print obj.GetTitle(), obj.GetName()

    h_orig[i] = obj.Clone();
    h[i] = obj.Clone(); h[i].SetName(obj.GetName()+"_Down")    

    #for b in range(h[i].GetNbinsX()):
    for b in range(0,len(bins)):
      #h_orig[i].SetBinContent(b+1, 1+h[i].GetBinContent(b+1))
      #h[i].SetBinContent(b+1, 1-h[i].GetBinContent(b+1))
      h_orig[i].SetBinContent(b,1+h[i].GetBinContent(h[i].FindBin(bins[b])))
      h[i].SetBinContent(b,1-h[i].GetBinContent(h[i].FindBin(bins[b])))
      print b,h[i].GetXaxis().GetBinCenter(b), h[i].GetBinContent(b)

      #print s, b+1, h_orig[i].GetBinContent(b+1), h[i].GetBinContent(b+1)

    h[i].SetMaximum(1.1)
    h[i].SetMinimum(0.9)
    h_orig[i].SetMaximum(1.1)
    h_orig[i].SetMinimum(0.9)
    f_out.cd()
    h_orig[i].Write()
    h[i].Write()

    hv[i] = TH1F(h[i].GetName()+"_monov",h[i].GetName()+"_monov",len(bins_monov)-1,array('d',bins_monov))
    hv_orig[i] = TH1F(h_orig[i].GetName()+"_monov",h_orig[i].GetName()+"_monov",len(bins_monov)-1,array('d',bins_monov))

    for b in range(0,len(bins_monov)):
      hv[i].SetBinContent(b,h[i].GetBinContent(h[i].FindBin(bins_monov[b])))
      hv_orig[i].SetBinContent(b,h_orig[i].GetBinContent(h_orig[i].FindBin(bins_monov[b])))
      #print b,h[i].GetXaxis().GetBinCenter(b), h[i].GetBinContent(b)
      
    hv[i].Write()
    hv_orig[i].Write()

    i+1

  f_out.Close()

################################

makevariations()
#makevariations('wtoz')
