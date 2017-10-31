import ROOT
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")
from HiggsAnalysis.CombinedLimit.ModelTools import *

cat  = "monojet"
#cat  = "monov"

if cat is "monojet":
  th1name = "hQCD_MonoJ"
else:
  th1name = "hQCD_MonoV"

fdir = ROOT.TFile('templates_12p9_250rebinned.root','READ')

wsin_combine = ROOT.RooWorkspace("monoxQCD","monoxQCD")
wsin_combine._import = SafeWorkspaceImporter(wsin_combine)#getattr(wsin_combine,"import")
 
samplehistos = fdir.GetListOfKeys()
for s in samplehistos: 
  obj = s.ReadObj()
  if type(obj)!=type(ROOT.TH1F()): continue
  if obj.GetTitle().startswith(th1name): continue # Forget all of the histos which aren't the observable variable
  #if 'All' not in  obj.GetTitle() : continue
  if 'nominal' not in  obj.GetName() : continue
  samplehist = obj
  break
nbins = samplehist.GetNbinsX()

varl = ROOT.RooRealVar("met_"+cat,"met_"+cat,0,100000);

# Keys in the fdir 
keys_local = fdir.GetListOfKeys() 
for key in keys_local: 
  obj = key.ReadObj()
  print obj.GetName(), obj.GetTitle(), type(obj)
  if type(obj)!=type(ROOT.TH1F()): continue
  title = obj.GetTitle()
  if not title.startswith(th1name): continue # Forget all of the histos which aren't the observable variable
  name = obj.GetName()
  if not obj.Integral() > 0 : obj.SetBinContent(1,0.0001) # otherwise Combine will complain!
  print "Scaling by the lumi increase"
  obj.Scale(2.84)
  print "Creating Data Hist for ", name 
  #dhist = ROOT.RooDataHist("%s_signal_%s"%(cat,name),"Dataset for qcd in monojet SR",ROOT.RooArgList(varl),obj)#cat+"_"+name,"DataSet - %s, %s"%(cat,name),ROOT.RooArgList(varl),obj)
  if "nominal" in name:
    dhist = ROOT.RooDataHist("%s_signal_qcd"%(cat),"Dataset for qcd in monojet SR",ROOT.RooArgList(varl),obj)#cat+"_"+name,"DataSet - %s, %s"%(cat,name),ROOT.RooArgList(varl),obj)
  else:
    if cat in 'monov':
      name = name.replace("hQCD_MonoV_","")
      print "monov",name
      dhist = ROOT.RooDataHist("%s_signal_qcd_%s"%(cat,name),"Dataset for qcd in monojet SR",ROOT.RooArgList(varl),obj)#cat+"_"+name,"DataSet - %s, %s"%(cat,name),ROOT.RooArgList(varl),obj)
    else:
      name = name.replace("hQCD_MonoJ_","")
      print name
      dhist = ROOT.RooDataHist("%s_signal_qcd_%s"%(cat,name),"Dataset for qcd in monojet SR",ROOT.RooArgList(varl),obj)#cat+"_"+name,"DataSet - %s, %s"%(cat,name),ROOT.RooArgList(varl),obj)

  #dhist.Print("v")

  wsin_combine._import(dhist)

wsin_combine.writeToFile("ws_250bin/%s_qcd.root"%(cat))

