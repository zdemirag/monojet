#! /usr/bin/env python
from ROOT import *
#from colors import *
#colors = defineColors()

lumi = 1.0

######################################################

dataDir = "/afs/cern.ch/work/z/zdemirag/public/moriond17/setup80x/vbf_panda/vbf_004_7/"

physics_processes = {
        
        'QCD'               : { 'label':'QCD',
                                'datacard':'qcd',
                                'color' : "#FDFEFE" , 
                                'ordering': 0,
                                'xsec' : 1.0,
                                'files':[dataDir+'QCD.root'],
                                },

        'Zll'               : { 'label'   : 'Z#rightarrow ll',
                                'datacard': 'Zll',
                                'color'   : "#F08080", 
                                'ordering': 1,                  
                                'xsec'    : 1.0,
                                'files'   : [dataDir+"ZJets.root"],
                                },

#       'EWKZ2Jets_ZToLL'   : { 'label':'EWK Z(ll) + 2jets',
#                               'datacard':'ewk_zll',
#                               'color'   :"#CD5C5C",
#                               'ordering': 2,
#                               'xsec' : 1.0,
#                               'files':[dataDir+'ZJets_EWK.root',],
#                               },               

        'Top'              : { 'label':'Top quark',
                                'datacard':'ttbar',
                                'color' : "#FFD700",
                                'ordering': 2,
                                'xsec' : 1.0,
                                'files':[dataDir+'TopQuark.root',],
                                },        

        'Diboson'           : { 'label':'Diboson',
                               'datacard':'diboson',
                               'color':"#DAA520",
                               'ordering': 3,
                               'xsec' : 1.0,
                               'files':[dataDir+'Diboson.root',],
                                },

        'Wlv'               : { 'label'   : 'W#rightarrow  l#nu',
                                'datacard': 'Wlv',
                                'color'   : "#E6E6FA", 
                                'ordering': 5,
                                'xsec'    : 1.0,
                                'files'   : [dataDir+'WJets.root',],
                                },

#        'EWKW'              : { 'label'   : 'EWK W + 2jets',
#                                'datacard': 'ewk_w',
#                                'color'   : "#9370DB",
#                                'ordering': 4,
#                                'xsec'    : 1.0,
#                                'files'   : [dataDir+'WJets_EWK.root',],
#                                },       

        'Zvv'               : { 'label'   : 'Z#rightarrow#nu#nu', 
                                'datacard': 'Zvv', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : 1.0,
                                'files'   : [dataDir+"ZtoNuNu.root"],
                                },

#       'EWKZ2Jets_ZToNuNu' : { 'label'    : 'EWK Z(#nu#nu) + 2jets',
#                               'datacard' : 'ewk_znn',
#                               'color'    : "#4682B4",
#                               'ordering' : 6,
#                               'xsec'     : 1.0,
#                               'files'    : [dataDir+'ZtoNuNu_EWK.root',],
#                               },       
        
        'data'              : { 'label':'Data',
                                'datacard':'data',
                                'color': 1,
                                'ordering': 8,    
                                'xsec' : 1.0,                  
                                'files':[dataDir+'SingleElectron.root',],                  
                                },
        
        'signal_vbf'        : {'label':'qqH 125',
                               'datacard':'signal',
                               'color':1,
                               'ordering': 9,
                               'xsec' : 1.0,
                               'files':[dataDir+'vbfHinv_m125.root',],
                               },
        
        'signal_ggf'        : {'label':'ggH 125',
                               'datacard':'signal',
                               'color':1,
                               'ordering': 9,
                               'xsec' : 1.0,
                               'files':[dataDir+'ggFHinv_m125.root',],
                               }
        
        }

tmp = {}
for p in physics_processes: 
	if physics_processes[p]['ordering']>-1: tmp[p] = physics_processes[p]['ordering']
ordered_physics_processes = []

for key, value in sorted(tmp.iteritems(), key=lambda (k,v): (v,k)):
	ordered_physics_processes.append(key)

def makeTrees(process,tree,channel):
	Trees={}
	Trees[process]   = TChain(tree)
	for sample in  physics_processes[process]['files']:
		Trees[process].Add(sample)
	return Trees[process]

######################################################


'''

'''
