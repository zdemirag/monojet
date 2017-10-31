#! /usr/bin/env python                                                                                                                                                              
from ROOT import *
from array import array
#from tdrStyle import *
import math
#from pretty import plot_cms
#setTDRStyle()

def makevariations(model):

  bins = [ 250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0]
  bins_test = [250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0]
  bins_monov = [250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 750, 1000.0]
  
  if model == "pdf":
    infile = TFile("/afs/cern.ch/user/z/zdemirag/public/forRaffaele/new_sys/out_pdf.root","READ")
    f_out = TFile("wtow_pdf_sys3.root","recreate")

  if model == "veto":
    infile = TFile("/afs/cern.ch/user/z/zdemirag/public/forRaffaele/new_sys/out_veto.root","READ")
    f_out = TFile("veto_sys3.root","recreate")

  if model == "trigger":
    infile = TFile("/afs/cern.ch/user/z/zdemirag/public/forRaffaele/new_sys/out_triggersys.root","READ")
    f_out = TFile("trigger_sys3.root","recreate")

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
    h[i] = obj.Clone(); h[i].SetName(obj.GetName()+"_Down")    


    hmj[i] = TH1F(h[i].GetName(),h[i].GetName(),len(bins)-1,array('d',bins))
    hmj_orig[i] = TH1F(h_orig[i].GetName(),h_orig[i].GetName(),len(bins)-1,array('d',bins))

    #for b in range(h[i].GetNbinsX()):
    for b in range(0,len(bins)):
      hmj_orig[i].SetBinContent(b,h[i].GetBinContent(h[i].FindBin(hmj[i].GetBinCenter(b))))
      hmj[i].SetBinContent(b,2-h[i].GetBinContent(h[i].FindBin(hmj[i].GetBinCenter(b))))
      print b, bins[b], hmj_orig[i].GetBinContent(b), hmj[i].GetBinContent(b)

      #print s, b+1, h_orig[i].GetBinContent(b+1), h[i].GetBinContent(b+1)

    hmj[i].SetMaximum(1.1)
    hmj[i].SetMinimum(0.9)
    hmj_orig[i].SetMaximum(1.1)
    hmj_orig[i].SetMinimum(0.9)
    f_out.cd()
    hmj_orig[i].Write()
    hmj[i].Write()

    hv[i] = TH1F(h[i].GetName()+"_monov",h[i].GetName()+"_monov",len(bins_monov)-1,array('d',bins_monov))
    hv_orig[i] = TH1F(h_orig[i].GetName()+"_monov",h_orig[i].GetName()+"_monov",len(bins_monov)-1,array('d',bins_monov))

    for b in range(0,len(bins_monov)):
      hv[i].SetBinContent(b,2-h[i].GetBinContent(h[i].FindBin( hv[i].GetBinCenter(b) )))
      hv_orig[i].SetBinContent(b,h_orig[i].GetBinContent(h_orig[i].FindBin( hv[i].GetBinCenter(b) )))
      
    hv[i].Write()
    hv_orig[i].Write()

    i+1

  f_out.Close()

################################

makevariations("pdf")
makevariations("trigger")
makevariations("veto")
