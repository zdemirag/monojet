#! /usr/bin/env python                                                                                                                                                              
from ROOT import *
from array import array
import math

def makevariations(cat):

  #bins = [250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1249.0]
  bins = [230., 260.0, 290.0, 320.0, 350.0, 390.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0,1400.0]
  bins_monov = [250.0, 300.0, 350.0, 400.0, 500.0, 600.0, 750, 1000.0]
  
  #f_in = TFile("trigger_sys_230bin.root","read")
  #f_out = TFile("fixtrig"+cat+"230bin.root","recreate")
  f_in = TFile("trigger_sys3.root","read")
  f_out = TFile("fixtrig"+cat+"3.root","recreate")
  zmm = f_in.Get("zmm_sys"+cat)
  zvv = f_in.Get("zvv_sys"+cat)

  #zmm.Divide(zvv)
  zvv.Divide(zmm)
  zvv_up = zmm.Clone("down")
  for b in range(0,len(bins)):
      if (b == zvv.FindBin(520) or b>zvv.FindBin(520)):
          zvv.SetBinContent(b,1)
      zvv_up.SetBinContent(b,2-zvv.GetBinContent(b))

  zvv.SetName("trig_sys_down"+cat)
  zvv_up.SetName("trig_sys_up"+cat)
  zvv.Write()
  zvv_up.Write()
  f_out.Close()

################################

makevariations("")
makevariations("_monov")
