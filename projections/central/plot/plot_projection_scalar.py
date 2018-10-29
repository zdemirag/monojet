from ROOT import *
from array import array
from tdrStyle import *
setTDRStyle()

import math

lumiScale = "4"

def make_tgraph(opt):
    
    curve = []
    mass  = []

    if opt is 'l1':
        filename = '../scalar/ls1/ls1_scalar.root'

    elif opt is 'l100':
        filename = '../scalar/ls'+lumiScale+'/all/ls'+lumiScale+'_all_scalar.root'

    elif opt is 'l100_exp':
        filename = '../scalar/ls'+lumiScale+'/experiment/ls'+lumiScale+'_exp_scalar.root'

    elif opt is 'l100_the':
        filename = '../scalar/ls'+lumiScale+'/theory/ls'+lumiScale+'_the_scalar.root'

    else:
        print "No option specified"

    print filename
    f = ROOT.TFile.Open(filename)
    for event in f.limit:
        if event.quantileExpected == 0.5:
            print float(str(event.mh)[7:])
            if (float(str(event.mh)[7:]) == 1.0) :
                m = str(event.mh)[3:7]
                if float(m) == 125.0 : continue
                if float(m) == 100.0 : continue
                if float(m) < 40.0 : continue
                if float(m) > 600.0 : continue
                mass.append(float(m))
                curve.append(event.limit)
                print filename, m, event.limit 

    finalcurve = array('d',curve)                                    
    finalmass  = array('d',mass)

    v_mass = ROOT.TVectorD(len(finalmass),finalmass)                                                            
    v_exp  = ROOT.TVectorD(len(finalcurve),finalcurve)  
    gr_exp = ROOT.TGraph(v_mass,v_exp)          
    
    return gr_exp, finalcurve, v_mass
        
def plot_projection():

    c = TCanvas("c","c",600,600)  
    c.cd()
    #c.SetLogx()
    c.SetLogy()

    dummy = ROOT.TH1D("dummy","dummy", 0, 20, 640)
    dummy.GetXaxis().SetTitle('med_{mass} [GeV]')   
    dummy.GetYaxis().SetTitle('95%  CL upper limit on #sigma/#sigma_{theory}')   
    dummy.SetLineColor(0)
    dummy.SetLineWidth(0)
    dummy.SetFillColor(0)
    dummy.SetMinimum(0.1)
    dummy.SetMaximum(50)
    dummy.Draw()    

    gr_l1        , ary_l1        , vec_massl1       = make_tgraph('l1')
    gr_l100      , ary_l100      , vec_massl100     = make_tgraph('l100')
    gr_l100_exp  , ary_l100_exp  , vec_massl100_exp = make_tgraph('l100_exp')
    gr_l100_the  , ary_l100_the  , vec_massl100_the = make_tgraph('l100_the')


    vec_l1 = ROOT.TVectorD(len(ary_l1),ary_l1)  
    gr_l1  = ROOT.TGraph(vec_massl1,vec_l1)        

    vec_l100 = ROOT.TVectorD(len(ary_l100),ary_l100)  
    gr_l100  = ROOT.TGraph(vec_massl100,vec_l100)        

    vec_l100_exp = ROOT.TVectorD(len(ary_l100_exp),ary_l100_exp)  
    gr_l100_exp  = ROOT.TGraph(vec_massl100_exp,vec_l100_exp)        

    vec_l100_the = ROOT.TVectorD(len(ary_l100_the),ary_l100_the)  
    gr_l100_the  = ROOT.TGraph(vec_massl100_the,vec_l100_the)        
    
    #color1 = TColor.GetColor("#0868ac")
    #color2 = TColor.GetColor("#43a2ca")
    #color3 = TColor.GetColor("#7bccc4")
    #color4 = TColor.GetColor("#bae4bc")

    color1 = 2
    color2 = 4
    color3 = 8
    color4 = 1

    gr_l1.SetLineColor(color1)
    gr_l1.SetLineWidth(2)
    gr_l1.SetLineStyle(1)
    gr_l1.SetMarkerStyle(20)
    gr_l1.SetMarkerColor(color1)
    gr_l1.Draw("lpsame")

    gr_l100.SetLineColor(color2)
    gr_l100.SetLineWidth(2)
    gr_l100.SetLineStyle(1)
    gr_l100.SetMarkerStyle(22)
    gr_l100.SetMarkerColor(color2)
    gr_l100.Draw("lpsame")

    gr_l100_exp.SetLineColor(color3)
    gr_l100_exp.SetLineWidth(2)
    gr_l100_exp.SetLineStyle(1)
    gr_l100_exp.SetMarkerStyle(23)
    gr_l100_exp.SetMarkerColor(color3)
    gr_l100_exp.Draw("lpsame")

    gr_l100_the.SetLineColor(color4)
    gr_l100_the.SetLineWidth(2)
    gr_l100_the.SetLineStyle(1)
    gr_l100_the.SetMarkerStyle(4)
    gr_l100_the.SetMarkerColor(color4)
    gr_l100_the.Draw("lpsame")

    gStyle.SetOptStat(0)

    legend = TLegend(0.50,.70,.92,.90)
    legend.AddEntry(gr_l1,"35.9 fb^{-1}, all unc.","lp")
    legend.AddEntry(gr_l100,"143.6 fb^{-1}, all unc.","lp")
    legend.AddEntry(gr_l100_exp,"143.6 fb^{-1}, no experimental unc.","lp")
    legend.AddEntry(gr_l100_the,"143.6 fb^{-1}, no theoretical unc.","lp")

    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    
    legend.Draw("same")
    
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.035)
    latex2.SetTextAlign(31) # align right
    latex2.DrawLatex(0.95, 0.95, "(13 TeV)");
    
    latex3 = TLatex()
    latex3.SetNDC()
    latex3.SetTextSize(0.75*c.GetTopMargin())
    latex3.SetTextFont(62)
    latex3.SetTextAlign(11) # align right
    latex3.DrawLatex(0.17, 0.85, "CMS");
    latex3.SetTextSize(0.5*c.GetTopMargin())
    latex3.SetTextFont(52)
    latex3.SetTextAlign(11)
    latex3.DrawLatex(0.17, 0.8, "Work in progress");
    
    latex3.SetTextSize(0.3*c.GetTopMargin())
    latex3.SetTextFont(42)
    latex3.SetTextAlign(11)
    #latex3.DrawLatex(0.17, 0.75, "Scalar m_{med}= 125 GeV, g_{q}=1, g_{DM}=1");
    latex3.DrawLatex(0.17,0.75,"#bf{Scalar med, Dirac DM}")
    latex3.DrawLatex(0.17,0.70,"#bf{m_{DM} = 1 GeV g_{q} = 1, g_{DM} = 1}")
    #latex3.DrawLatex(0.17, 0.75, "Scalar g_{q}=1, g_{DM}=1");

    #if folder.startswith('experiment'):
    #    latex3.DrawLatex(0.17, 0.70, "x0.5 Experimental uncertainties");

    #if folder.startswith('theory'):
    #    latex3.DrawLatex(0.17, 0.70, "x0.5 Theoretical uncertainties");

    gPad.RedrawAxis()
    
    topfolder = "/afs/cern.ch/user/z/zdemirag/www/monojet_projections/"
    c.SaveAs(topfolder+"/projection_scalar_1D_ls"+lumiScale+".pdf")
    c.SaveAs(topfolder+"/projection_scalar_1D_ls"+lumiScale+".png")
    c.SaveAs(topfolder+"/projection_scalar_1D_ls"+lumiScale+".C")
    c.SaveAs(topfolder+"/projection_scalar_1D_ls"+lumiScale+".root")

    del c
 
plot_projection()
plot_projection()
plot_projection()
