#! /usr/bin/env python
from ROOT import *
#from colors import *
#colors = defineColors()

lumi = 1.0

######################################################

dataDir ="/afs/cern.ch/work/z/zdemirag/public/moriond17/setup80x/vbf_panda/vbf_004_7/"

physics_processes = {
        
        'QCD'               : { 'label':'QCD',
                                'datacard':'qcd',
                                'color' : "#FDFEFE" , 
                                'ordering': 0,
                                'xsec' : 1.0,
                                'files':[dataDir+'QCD.root'],
                                },

        'GJets'             : { 'label'   : '#gamma + jets', 
                                'datacard': 'Gjets', 
                                'color'   : "#B0C4DE",
                                'ordering': 7,
                                'xsec'    : 1.0,
                                'files'   : [dataDir+"GJets.root"],
                                },

        'data'              : { 'label':'Data',
                                'datacard':'data',
                                'color': 1,
                                'ordering': 8,    
                                'xsec' : 1.0,                  
                                'files':[dataDir+'SinglePhoton.root',],                  
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
