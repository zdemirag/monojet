#! /usr/bin/env python
import sys, os, string, re, time, datetime
from multiprocessing import Process
from array import *
from ROOT import *
from math import *
from tdrStyle import *
from selection import build_selection, build_weights
from datacard import dump_datacard
from pretty import plot_ratio, plot_cms
import numpy as n
from LoadData import *
#from LoadElectron import *
#from LoadPhoton import *

#channel_list = ['signal']
channel_list  = ['Wmn']
#channel_list = ['Wen']
#channel_list = ['Zmm']
#channel_list = ['Zee']
#channel_list = ['GJets']

category = 'monojet'

lumi=35900. 
lumi_str = 35.9

blind = False

setTDRStyle()

gROOT.LoadMacro("functions.C+");

print "Starting Plotting Be Patient!"

def plot_stack(channel, name,var, bin, low, high, ylabel, xlabel, setLog = False):

    folder = '/afs/cern.ch/user/z/zdemirag/www/monojet/panda/v1'

    if not os.path.exists(folder):
        os.mkdir(folder)

    yield_dic = {}    

    stack = THStack('a', 'a')
    if var.startswith('pfmet') or var.startswith('pfU'):
        binLowE =  [ 250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0]
        nb = len(binLowE)-1
        added = TH1D('added','added',nb,array('d',binLowE))
    else:
        added = TH1D('added', 'added',bin,low,high)

    added.Sumw2()

    f  = {}
    h1 = {}

    Variables = {}
    cut_standard = build_selection(channel)

    if var.startswith('pfU'):
        if channel is not 'signal': 
            xlabel = 'Hadronic Recoil p_{T} [GeV]'

    print "INFO Channel is: ", channel, " variable is: ", var, " Selection is: ", cut_standard,"\n"
    print 'INFO time is:', datetime.datetime.fromtimestamp( time.time())

    reordered_physics_processes = []
    if channel == 'Zmm' or channel == 'Zee': 
        reordered_physics_processes = reversed(ordered_physics_processes)
    else: 
        reordered_physics_processes = ordered_physics_processes

    for Type in ordered_physics_processes:
        yield_dic[physics_processes[Type]['datacard']] = 0

    for Type in reordered_physics_processes:
        histName = Type+'_'+name+'_'+channel

        if var.startswith('pfmet') or var.startswith('pfU'):
            binLowE =  [ 250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0]
            n2 = len(binLowE)-1
            Variables[Type] = TH1F(histName,histName,n2,array('d',binLowE))
        else:
            Variables[Type] = TH1F(histName, histName, bin, low, high)
        
        Variables[Type].Sumw2()
        Variables[Type].StatOverflows(kTRUE)

        input_tree   = makeTrees(Type,"events",channel)
        n_entries = input_tree.GetEntries()

        scale = float(lumi) # *physics_processes[Type]['xsec']/total

        common_weight = build_weights(channel,Type)

        print Type, common_weight, scale

        if Type is not 'data' and Type is not 'signal_ggf' and Type is not 'signal_vbf':            

            Variables[Type].SetFillColor(TColor.GetColor(physics_processes[Type]['color']))
            Variables[Type].SetLineColor(1)        

            makeTrees(Type,'events',channel).Draw(var + " >> " + histName,"(" + cut_standard+ " )"+common_weight,"goff")

            if var == "pfmet" or var.startswith('pfU'):
                nbins = Variables[Type].GetNbinsX()
                Variables[Type].SetBinContent(Variables[Type].GetNbinsX(),Variables[Type].GetBinContent(nbins)+Variables[Type].GetBinContent(nbins+1))

            Variables[Type].Scale(scale,"width")
            stack.Add(Variables[Type],"hist")
            added.Add(Variables[Type])

        if Type.startswith('signal'):
            makeTrees(Type,'events',channel).Draw(var + " >> " + histName,"(" + cut_standard + ")"+common_weight,"goff")
            if var == "pfmet" or var.startswith('pfU'):
                nbins = Variables[Type].GetNbinsX()
                Variables[Type].SetBinContent(Variables[Type].GetNbinsX(),Variables[Type].GetBinContent(nbins)+Variables[Type].GetBinContent(nbins+1))
            Variables[Type].Scale(scale,"width")

        if Type.startswith('data'):
            Variables[Type].SetMarkerStyle(20)
            if channel in 'signal' or channel in 'Zmm' or channel in 'Wmn':
                #met trigger
                makeTrees(Type,"events",channel).Draw(var + " >> " + histName, "(" + cut_standard + "&& (trigger&1)!=0)", "goff")  
            elif channel in 'GJets':
                #photon trigger - no need, the flag is not working properly
                makeTrees(Type,"events",channel).Draw(var + " >> " + histName, cut_standard , "goff")  
            else:
                #ele trigger
                makeTrees(Type,"events",channel).Draw(var + " >> " + histName, "(" + cut_standard + "&& (trigger&2)!=0)", "goff")  
                

            if var == "pfmet" or var.startswith('pfU'):
                nbins = Variables[Type].GetNbinsX()
                Variables[Type].SetBinContent(Variables[Type].GetNbinsX(),Variables[Type].GetBinContent(nbins)+Variables[Type].GetBinContent(nbins+1))
            Variables[Type].Scale(1,"width")

        yield_dic[physics_processes[Type]['datacard']] += round(Variables[Type].Integral("width"),3)

    dump_datacard(channel,yield_dic)
            
    print 'INFO - Drawing the Legend', datetime.datetime.fromtimestamp( time.time())

    if channel is 'GJets':
        legend = TLegend(.60,.65,.82,.92)
    else:
        legend = TLegend(.60,.55,.92,.92)

    lastAdded  = ''
    for process in  ordered_physics_processes:
        Variables[process].SetTitle(process)
        if physics_processes[process]['label'] != lastAdded:
            lastAdded = physics_processes[process]['label']
            if process is not 'data' and process is not 'signal_vbf' and process is not 'signal_ggf':
                legend . AddEntry(Variables[process],physics_processes[process]['label'] , "f")
            if process is 'data':
                legend . AddEntry(Variables[process],physics_processes[process]['label'] , "p")

    c4 = TCanvas("c4","c4", 600, 700)
    c4.SetBottomMargin(0.3)
    c4.SetRightMargin(0.06)
    stack.SetMinimum(0.01)

    if setLog:
        c4.SetLogy()
        if "eta" in var:
            stack.SetMaximum( Variables['data'].GetMaximum()  +  1e8*Variables['data'].GetMaximum() )
        else:
            stack.SetMaximum( Variables['data'].GetMaximum()  +  1e2*Variables['data'].GetMaximum() )

    else:
        stack.SetMaximum( Variables['data'].GetMaximum()  +  0.5*Variables['data'].GetMaximum() )
    
    stack.Draw()
    stack.GetYaxis().SetTitle(ylabel)
    stack.GetYaxis().CenterTitle()
    stack.GetYaxis().SetTitleOffset(1.2)
    stack.GetXaxis().SetTitleOffset(1.2)
    stack.GetXaxis().SetTitle(xlabel)
    stack.GetXaxis().SetLabelSize(0)
    stack.GetXaxis().SetTitle('')
    
    if channel is 'signal' and blind:
         for b in range(Variables['data'].GetNbinsX()):
             Variables['data'].SetBinContent(b+1,0.0)

    Variables['data'].Draw("Esame")  
    Variables['signal_vbf'].SetLineWidth(2)
    Variables['signal_ggf'].SetLineWidth(2)
    Variables['signal_vbf'].SetLineColor(1)
    Variables['signal_ggf'].SetLineColor(4)
    #Variables['signal_vbf'].Draw("samehist")
    #Variables['signal_ggf'].Draw("samehist")

    #legend . AddEntry(Variables['signal_vbf'],physics_processes['signal_vbf']['label'] , "l")
    #legend . AddEntry(Variables['signal_ggf'],physics_processes['signal_ggf']['label'] , "l")

    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);

    legend.Draw("same")
    plot_cms(True,lumi_str,c4)


    Pad = TPad("pad", "pad", 0.0, 0.0, 1.0, 0.9)
    Pad.SetTopMargin(0.7)
    Pad.SetRightMargin(0.06)
    Pad.SetFillColor(0)
    Pad.SetGridy(1)
    Pad.SetFillStyle(0)
    Pad.Draw()
    Pad.cd(0)

    data = Variables['data'].Clone()

    plot_ratio(False,data,added,bin,xlabel,0.5,1.5,5)

    f1 = TF1("f1","1",-5000,5000);
    f1.SetLineColor(4);
    f1.SetLineStyle(2);
    f1.SetLineWidth(2);
    f1.Draw("same")

    Pad.Update()
    Pad.RedrawAxis()

    c4.SaveAs(folder+'/Histo_'+category+'_' + name + '_'+channel+'.pdf')
    c4.SaveAs(folder+'/Histo_'+category+'_' + name + '_'+channel+'.png')
    c4.SaveAs(folder+'/Histo_'+category+'_' + name + '_'+channel+'.C')

    del Variables
    del var
    del f
    del h1
    c4.IsA().Destructor( c4 )
    stack.IsA().Destructor( stack )

arguments = {}
#                   = [var, bin, low, high, yaxis, xaxis, setLog]
arguments['pfmet']      = ['pfmet','pfmet',100,200,3500,'Events/GeV','E_{T}^{miss} [GeV]',True]
arguments['metphi']     = ['pfmetphi','pfmetphi',25,-5,5,'Events','E_{T}^{miss} #Phi [GeV]',True]
arguments['dphipfmet']  = ['dphipfmet','dphipfmet',50,0,5,'Events','#Delta #Phi(jet,E_{T}^{miss})',False]

arguments['pfUZmag']    = ['pfUZmag','pfUZmag',100,200,3500,'Events/GeV','E_{T}^{miss} (Z Recoil) [GeV]',True]
arguments['pfUZphi']    = ['pfUZphi','pfUZphi',25,-5,5,'Events','E_{T}^{miss} #Phi (Z Recoil) [GeV]',False]
arguments['dphipfUZ']   = ['dphipfUZ','dphipfUZ',50,0,5,'Events','#Delta #Phi(jet,E_{T}^{miss})',False]

arguments['pfUWmag']    = ['pfUWmag','pfUWmag',100,200,3500,'Events/GeV','E_{T}^{miss} (W Recoil) [GeV]',True]
arguments['pfUWphi']    = ['pfUWphi','pfUWphi',25,-5,5,'Events','E_{T}^{miss} #Phi (W Recoil) [GeV]',False]
arguments['dphipfUW']   = ['dphipfUW','dphipfUW',50,0,5,'Events','#Delta #Phi(jet,E_{T}^{miss})',False]

arguments['pfUAmag']    = ['pfUAmag','pfUAmag',100,200,3500,'Events/GeV','E_{T}^{miss} (#gamma Recoil) [GeV]',True]
arguments['pfUAphi']    = ['pfUAphi','pfUAphi',25,-5,5,'Events','E_{T}^{miss} #Phi (#gamma Recoil) [GeV]',False]
arguments['dphipfUA']   = ['dphipfUA','dphipfUA',50,0,5,'Events','#Delta #Phi(jet,E_{T}^{miss})',False]

arguments['calomet']    = ['calomet','calomet',50,0,2000,'Events/GeV','Calo E_{T}^{miss} [GeV]',True]

arguments['jet1pt']     = ['jet1Pt','jet1Pt',25,10,1500,'Events/GeV','Leading Jet P_{T} [GeV]',True]
arguments['jet1phi']    = ['jet1Phi','jet1Phi',25,-5,5,'Events','Leading Jet #phi',False]
arguments['jet1eta']    = ['jet1eta','jet1Eta',25,-5,5,'Events','Leading Jet #eta',True]


arguments['npv']        = ['npv','npv',50,0,50,'Events','Number of primary vertices',False]
arguments['njet']       = ['nJet','nJet',10,0,10,'Events','Number of jets',False]

arguments['dphicalopf'] = ['dphicalopf','deltaPhi(calometphi,pfmetphi)',50,0,5,'Events','#Delta#phi_{calomet,pfmet}',False]
arguments['mT']         = ['mT','mT',40,0,400,'Events/GeV','MT',True]

arguments['diffmetW']   = ['diffmetW','fabs(calomet-pfmet)/pfUWmag',50,0,2,'Events','|Calo E_{T}^{miss} - PF E_{T}^{miss} | / Hadronic recoil P_{T}',True]

arguments['lep1pt']       = ['lep1pt','looseLep1Pt',25,0,1500,'Events/GeV','Leading lepton P_{T} [GeV]',True]
arguments['lep1eta']      = ['lep1eta','looseLep1Eta',25,-5,5,'Events','Leading Lepton #eta',True]

processes     = []

variable_list = []

#variable_list = ['pfUAmag']
#variable_list = ['jet1pt','jet1eta','pfmet','pfUWmag','dphipfmet','calomet','jet1phi','npv','njet','mT','lep1pt']
#variable_list = ['pfmet','npv']
#variable_list = ['lep1eta']

if 'Zmm' in channel_list or 'Zee' in channel_list:
    variable_list.append('pfUZmag')    
    
if 'Wmn' in channel_list or 'Wen' in channel_list:
    variable_list.append('pfUWmag')

if 'GJets' in channel_list:
    variable_list.append('pfUAmag')

if 'signal' in channel_list:
    variable_list.append('pfmet')

start_time = time.time()

for channel in channel_list:
    for var in variable_list:
        print var
        arguments[var].insert(0,channel)
        print  arguments[var]
        process = Process(target = plot_stack, args = arguments[var])
        process.start()
        processes.append(process)
        arguments[var].remove(channel)
for process in processes: 
    process.join()

print("--- %s seconds ---" % (time.time()-start_time))
print datetime.datetime.fromtimestamp(time.time()-start_time)
