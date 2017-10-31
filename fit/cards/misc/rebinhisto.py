#! /usr/bin/env python                                                                                                                                                              
from ROOT import *
from array import array
#from tdrStyle import *
import math
#from pretty import plot_cms
#setTDRStyle()

def makevariations(model):

  bins = [ 250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0]
  #bins_test = [ 250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1249.0]

  bins_monov = [250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 750, 1000.0]  
  #bins = [230., 260.0, 290.0, 320.0, 350.0, 390.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0]
  #bins_test = [230., 260.0, 290.0, 320.0, 350.0, 390.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1249.0]

  if model == "purity":

    infile = TFile("purity_monojet.root","READ")
    f_out = TFile("purity_monojet_250rebinned.root","recreate")

  if model == "qcd":

    infile = TFile("templates_12p9.root","READ")
    f_out = TFile("templates_12p9_250rebinned.root","recreate")


  h_orig = {}
  h = {}
  hmj_orig = {}
  hmj = {}
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

    hmj_orig[i] = TH1F(h_orig[i].GetName(),h_orig[i].GetName(),len(bins)-1,array('d',bins))

    for b in range(0,len(bins)):
      hmj_orig[i].SetBinContent(b,h_orig[i].GetBinContent(h_orig[i].FindBin(bins[b])))
      #hmj_orig[i].SetBinContent(b,h_orig[i].GetBinContent(h_orig[i].FindBin(h_orig[i].GetBinCenter(b+1))))
      
    f_out.cd()
    hmj_orig[i].Write()

    i+1

  f_out.Close()

################################

makevariations('purity')
makevariations('qcd')
