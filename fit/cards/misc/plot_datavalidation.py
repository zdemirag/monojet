from ROOT import *
from collections import defaultdict
import math, os
from math import sqrt, pow
from array import array
from tdrStyle import *
setTDRStyle()


def dataValidation(region1,region2,category,unc):

    if region1 is "combined" and region2 is "gjets":
        name = "Z(ll)/#gamma"
    if region1 is "combined" and region2 is "combinedW":
        name = "Z(ll)/W"
    if region1 is "dielectron" and region2 is "gjets":
        name = "Z(ee)/#gamma"
    if region1 is "dimuon" and region2 is "gjets":
        name = "Z(mm)/#gamma"
    if region1 is "combinedW" and region2 is "gjets":
        name = "W(ln)/#gamma"
    if region1 is "singleelectron" and region2 is "gjets":
        name = "W(en)/#gamma"
    if region1 is "singlemuon" and region2 is "gjets":
        name = "W(mn)/#gamma"
    if region1 is "dielectron" and region2 is "singleelectron":
        name = "Z(ee)/W(en)"
    if region1 is "dimuon" and region2 is "singlemuon":
        name = "Z(mm)/W(mn)"



    datalab = {"singlemuon":"Wmn", "dimuon":"Zmm", "gjets":"gjets", "signal":"signal", "singleelectron":"Wen", "dielectron":"Zee"}
  
    f_data = TFile("mono-x.root","READ")
    f_data.cd("category_"+category)

    if region1 is "combined":
        h_data_1 = gDirectory.Get("Zmm_data")
        h_data_1_b = gDirectory.Get("Zee_data")
        h_data_1.Add(h_data_1_b)
    elif region1 is "combinedW":
        h_data_1 = gDirectory.Get("Wmn_data")
        h_data_1_b = gDirectory.Get("Wen_data")
        h_data_1.Add(h_data_1_b)

    else:
        h_data_1 = gDirectory.Get(datalab[region1]+"_data")
    h_data_1.Sumw2()
    if not category is "monov":
        h_data_1.Rebin(2)

    if region2 is "combinedW":    
        h_data_2 = gDirectory.Get("Wmn_data")
        h_data_2_b = gDirectory.Get("Wen_data")
        h_data_2.Add(h_data_2_b)
    else:
        h_data_2 = gDirectory.Get(datalab[region2]+"_data")

    h_data_2.Sumw2()
    if not category is "monov":
        h_data_2.Rebin(2)

    h_data_1.Divide(h_data_2)

    f_mlfit = TFile('mlfit.root','READ')

    channel = {"singlemuon":category+"_singlemu", "dimuon":category+"_dimuon", "gjets":category+"_photon", "signal":category+"_signal", "singleelectron":category+"_singleel", "dielectron":category+"_dielec"}

    h_prefit = {}

    if region1 is "combined":    
        h_prefit[region1] = f_mlfit.Get("shapes_prefit/"+category+"_dimuon/total_background")
        h_mc_2 = f_mlfit.Get("shapes_prefit/"+category+"_dielec/total_background")
        h_prefit[region1].Add(h_mc_2)
    elif region1 is "combinedW":    
        h_prefit[region1] = f_mlfit.Get("shapes_prefit/"+category+"_singlemu/total_background")
        h_mc_2 = f_mlfit.Get("shapes_prefit/"+category+"_singleel/total_background")
        h_prefit[region1].Add(h_mc_2)
    else:
        h_prefit[region1] = f_mlfit.Get("shapes_prefit/"+channel[region1]+"/total_background")
    h_prefit[region1].Sumw2()
    if not category is "monov":
        h_prefit[region1].Rebin(2)

    if region2 is "combinedW":    
        h_prefit[region2] = f_mlfit.Get("shapes_prefit/"+category+"_singlemu/total_background")
        h_mc2_2 = f_mlfit.Get("shapes_prefit/"+category+"_singleel/total_background")
        h_prefit[region2].Add(h_mc2_2)
    else:
        h_prefit[region2] = f_mlfit.Get("shapes_prefit/"+channel[region2]+"/total_background")

    h_prefit[region2].Sumw2()
    if not category is "monov":
        h_prefit[region2].Rebin(2)
    
    h_prefit[region1].Divide(h_prefit[region2])
  
    #uncFile_ewk = TFile('/afs/cern.ch/work/z/zdemirag/work/combination/CMSSW_7_4_7/src/MonoX-1/files/atoz_ewkunc.root')

    if unc is not "orig":
        uncFile = TFile('/afs/cern.ch/work/z/zdemirag/work/combination/CMSSW_7_4_7/src/MonoX-1/files/theory_unc_ZW.root')
        uncertainties = [
            uncFile.ZW_QCDScale_met,
            uncFile.ZW_NLOEWK_met,
            uncFile.ZW_EWKSudakov_met,
            uncFile.ZW_QCDEWK_met
            ]

    else:
        if region2 is "gjets":
            uncFile     = TFile('/afs/cern.ch/work/z/zdemirag/work/combination/CMSSW_7_4_7/src/MonoX-1/files/new/atoz_unc.root')

            uncertainties = [
                uncFile.a_ewkcorr_overz_Upcommon,
                uncFile.znlo1_over_anlo1_pdfUp,
                uncFile.znlo1_over_anlo1_renScaleUp,
                uncFile.znlo1_over_anlo1_facScaleUp
                ]

        else:
            uncFile     = TFile('/afs/cern.ch/work/z/zdemirag/work/combination/CMSSW_7_4_7/src/MonoX-1/files/new/wtoz_unc.root')
            uncertainties = [
                uncFile.w_ewkcorr_overz_Upcommon,
                uncFile.znlo1_over_wnlo1_pdfUp,
                uncFile.znlo1_over_wnlo1_renScaleUp,
                uncFile.znlo1_over_wnlo1_facScaleUp
                ]

    
    
    print uncertainties

    for iBin in range(h_prefit[region1].GetNbinsX()):
        if iBin == 0:
            continue
        #sumw2 = math.pow((h_prefit[region1].GetBinError(iBin)),2)
        sumw2 = pow((h_prefit[region1].GetBinError(iBin)),2)
        
        for uncert in uncertainties:
            findbin =  uncert.FindBin(h_prefit[region1].GetBinCenter(iBin))
            #print h_prefit[region1].GetBinCenter(iBin), uncert.FindBin(h_prefit[region1].GetBinCenter(iBin)),  uncert.GetBinContent(uncert.FindBin(h_prefit[region1].GetBinCenter(iBin))), uncert.GetBinContent(iBin)
            #sumw2 += math.pow((h_prefit[region1].GetBinContent(iBin) * (uncert.GetBinContent(findbin) - 1)),2)
            if unc is not "orig":
                sumw2 += pow((h_prefit[region1].GetBinContent(iBin) * (uncert.GetBinContent(findbin))),2)
            else:
                sumw2 += pow((h_prefit[region1].GetBinContent(iBin) * (uncert.GetBinContent(findbin) - 1)),2)
            
        h_prefit[region1].SetBinError(iBin,sqrt(sumw2))
        #h_prefit[region1].SetBinError(iBin,math.sqrt(sumw2))


    c = TCanvas("c","c")
    SetOwnership(c,False)

    c.cd()
    h_clone = h_prefit[region1].Clone()
    h_clone.SetFillColor(kGray) #SetFillColor(ROOT.kYellow)                                                                                                    
    h_clone.SetLineColor(kGray) #SetLineColor(1)                                                                                                              
    h_clone.SetLineWidth(1)
    h_clone.SetMarkerSize(0)
    h_clone.GetXaxis().SetTitle("Recoil [GeV]")
    h_clone.GetYaxis().SetTitle("Ratio "+name)
    h_clone.GetYaxis().SetTitleOffset(1.50)
    h_clone.SetMinimum(0)
    if region1 is "singlemuon" or "singlelectron":
        h_clone.SetMaximum(1.5)
    if region1 is "combinedW":
        h_clone.SetMaximum(2.5)
    if region1 is "dielectron":
        h_clone.SetMaximum(0.15)
    if region1 is "dimuon":
        h_clone.SetMaximum(0.2)
    if region2 is "singleelectron":
        h_clone.SetMaximum(0.4)
    if region2 is "singlemuon":
        h_clone.SetMaximum(0.4)
    if region1 is "combined":
        h_clone.SetMaximum(0.3)
    h_clone.Draw("e2")

    h_prefit[region1].SetLineColor(2)
    h_prefit[region1].Draw("samehist")
    h_data_1.SetLineColor(1)
    h_data_1.SetMarkerColor(1)
    h_data_1.SetMarkerStyle(20)
    h_data_1.Draw("same")


    legend = TLegend(0.50, 0.57, 0.92, .92);
    legend.SetFillStyle(0);
    legend.AddEntry(h_data_1, "Data Ratio", "p")
    legend.AddEntry(h_prefit[region1], "MC Ratio", "l")

    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.SetLineStyle(0);
    legend.SetBorderSize(0);
    legend.Draw("same")


    if unc is not "orig":
        c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond_80x/forAN_Dec21_v5/fits/nohltsafe/"+region1+"_"+region2+"_cat_"+category+"_aggresive_ratio.pdf")
        c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond_80x/forAN_Dec21_v5/fits/nohltsafe/"+region1+"_"+region2+"_cat_"+category+"_aggresive_ratio.png")
        c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond_80x/forAN_Dec21_v5/fits/nohltsafe/"+region1+"_"+region2+"_cat_"+category+"_aggresive_ratio.C")

    else:
        c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond_80x/forAN_Dec21_v5/fits/nohltsafe/"+region1+"_"+region2+"_cat_"+category+"_ratio.pdf")
        c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond_80x/forAN_Dec21_v5/fits/nohltsafe/"+region1+"_"+region2+"_cat_"+category+"_ratio.png")
        c.SaveAs("/afs/cern.ch/user/z/zdemirag/www/Monojet/moriond_80x/forAN_Dec21_v5/fits/nohltsafe/"+region1+"_"+region2+"_cat_"+category+"_ratio.C")



dataValidation("singleelectron","gjets","monojet","orig")
dataValidation("singlemuon","gjets","monojet","orig")
dataValidation("combinedW","gjets","monojet","orig")


#dataValidation("combined","gjets","monojet","orig")
#dataValidation("combined","combinedW","monojet","orig")

#dataValidation("dielectron","gjets","monojet","orig")
#dataValidation("dimuon","gjets","monojet","orig")
#dataValidation("dielectron","singleelectron","monojet","orig")
#dataValidation("dimuon","singlemuon","monojet","orig")

#dataValidation("combined","gjets","monov","orig")
#dataValidation("combined","combinedW","monov","orig")

#dataValidation("dielectron","gjets","monov","orig")
#dataValidation("dimuon","gjets","monov","orig")
#dataValidation("dielectron","singleelectron","monov","orig")
#dataValidation("dimuon","singlemuon","monov","orig")

#dataValidation("combined","combinedW","monojet","aggresive")
#dataValidation("dielectron","singleelectron","monojet","aggresive")
#dataValidation("dimuon","singlemuon","monojet","aggresive")

#dataValidation("combined","combinedW","monov","aggresive")

#dataValidation("dielectron","singleelectron","monov","aggresive")
#dataValidation("dimuon","singlemuon","monov","aggresive")
