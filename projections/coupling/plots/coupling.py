import ROOT
import sys
from array import array

ROOT.gROOT.ProcessLine(".L tdrstyle.C")
ROOT.setTDRStyle()
ROOT.gROOT.ProcessLine(".L useNiceColorPalette.C")
ROOT.useNiceColorPalette(255)

proc = "vector"

g_exp    = ROOT.TGraph2D()   

g_exp_l100     = ROOT.TGraph2D()   
g_exp_l100_exp = ROOT.TGraph2D()   
g_exp_l100_the = ROOT.TGraph2D()   

i=0
with open("limit_l1.txt","r") as f:
    for line in f:
        if line.startswith("#"): continue
        exp = line.split()[0]
        med = line.split()[1]
        coupling = line.split()[2]        
        #print exp, obs, med, coupling
        g_exp.SetPoint(i, float(med), float(coupling),float(exp))

        i = i+1

i=0
with open("limit_l100.txt","r") as f:
    for line in f:
        if line.startswith("#"): continue
        exp = line.split()[0]
        med = line.split()[1]
        coupling = line.split()[2]        
        #print exp, obs, med, coupling
        g_exp_l100.SetPoint(i, float(med), float(coupling),float(exp))

        i = i+1


i=0
with open("limit_l100_experiment.txt","r") as f:
    for line in f:
        if line.startswith("#"): continue
        exp = line.split()[0]
        med = line.split()[1]
        coupling = line.split()[2]        
        #print exp, obs, med, coupling
        g_exp_l100_exp.SetPoint(i, float(med), float(coupling),float(exp))

        i = i+1

i=0
with open("limit_l100_theory.txt","r") as f:
    for line in f:
        if line.startswith("#"): continue
        exp = line.split()[0]
        med = line.split()[1]
        coupling = line.split()[2]        
        #print exp, obs, med, coupling
        g_exp_l100_the.SetPoint(i, float(med), float(coupling),float(exp))

        i = i+1

print g_exp.GetN()

h_exp2          = g_exp.GetHistogram()
h_exp2_l100     = g_exp_l100.GetHistogram()
h_exp2_l100_exp = g_exp_l100_exp.GetHistogram()
h_exp2_l100_the = g_exp_l100_the.GetHistogram()

h_exp = h_exp2.Clone("h_exp");
h_exp_l100     = h_exp2_l100.Clone("h_exp2_l100");
h_exp_l100_exp = h_exp2_l100_exp.Clone("h_exp2_l100_exp");
h_exp_l100_the = h_exp2_l100_the.Clone("h_exp2_l100_the");

h_exp2.SetContour(2);
h_exp2.SetContourLevel(1, 1);

h_exp2_l100.SetContour(2);
h_exp2_l100.SetContourLevel(1, 1);
h_exp2_l100_exp.SetContour(2);
h_exp2_l100_exp.SetContourLevel(1, 1);
h_exp2_l100_the.SetContour(2);
h_exp2_l100_the.SetContourLevel(1, 1);

canvas = ROOT.TCanvas("canvas", "canvas", 1000, 800);
canvas.SetLogy()

frame = canvas.DrawFrame(0.0,0.01,3000,1,"")
frame.GetYaxis().SetTitle("g_{q}");
frame.GetXaxis().SetTitle("med_{mass} [GeV]");
frame.GetXaxis().SetTitleOffset(1.15);
frame.GetYaxis().SetTitleOffset(1.15);

ROOT.gStyle.SetLabelSize(0.035,"X");
ROOT.gStyle.SetLabelSize(0.035,"Y");
ROOT.gStyle.SetLabelSize(0.035,"Z");

frame.Draw()

h_exp2.SetLineStyle(2);
h_exp2.SetLineWidth(3);
h_exp2.Draw("CONT3 same");
h_exp2_l100.SetLineColor(2)
h_exp2_l100.Draw("CONT3 same")
h_exp2_l100_exp.Draw("CONT3 same")
h_exp2_l100_the.Draw("CONT3 same")


leg = ROOT.TLegend(0.36,0.62,0.80,0.88);#,NULL,"brNDC");
leg.AddEntry(h_exp2,"Median Expected (13 TeV) 95% CL","L");
#leg.AddEntry(h_obs2,"Observed (13 TeV) 95% CL","L");
leg.SetFillColor(0);
#leg.Draw("SAME");

tex = ROOT.TLatex();
tex.SetNDC();
tex.SetTextFont(42);
tex.SetLineWidth(2);
tex.SetTextSize(0.030);
tex.Draw();
tex.DrawLatex(0.68,0.96,"35.9 fb^{-1} (13 TeV)");
tex2 = ROOT.TLatex();
tex2.SetNDC();
tex2.SetTextFont(42);
tex2.SetLineWidth(2);
tex2.SetTextSize(0.042);
tex2.SetTextAngle(270);
#tex2.DrawLatex(0.965,0.93,"Observed    #sigma_{95% CL}/#sigma_{th}");

texCMS = ROOT.TLatex(0.22,0.96,"#bf{CMS}");
texCMS.SetNDC();
texCMS.SetTextFont(42);
texCMS.SetLineWidth(2);
texCMS.SetTextSize(0.042); texCMS.Draw();
ROOT.gPad.SetRightMargin(0.10);
#ROOT.gPad.SetTopMargin(0.05);
ROOT.gPad.SetBottomMargin(0.15);
ROOT.gPad.RedrawAxis();
ROOT.gPad.Modified(); 
ROOT.gPad.Update();

savefolder = "/afs/cern.ch/user/z/zdemirag/www/monojet_projections/"

canvas.SaveAs(savefolder+"coupling_"+proc+"_limits_all.pdf")
canvas.SaveAs(savefolder+"coupling_"+proc+"_limits_all.png")
