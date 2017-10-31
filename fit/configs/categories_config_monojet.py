# Configuration for a simple monojet topology. Use this as a template for your own Run-2 mono-X analysis
# First provide ouput file name in out_file_name field 

out_file_name = 'mono-x.root'

bins = [ 250.0, 280.0, 310.0, 340.0, 370.0, 400.0, 430.0, 470.0, 510.0, 550.0, 590.0, 640.0, 690.0, 740.0, 790.0, 840.0, 900.0, 960.0, 1020.0, 1090.0, 1160.0, 1250.0, 1400.0]

monojet_category = {
	    'name':"monojet"
            ,'in_file_name':"XXXX.root"
            ,"cutstring":"(met>250)"
            ,"varstring":["met",250,1400]
            ,"weightname":"weight"
            ,"bins":bins[:]
            ,"additionalvars":[['met',100,250,1400]]
            ,"pdfmodel":0
            ,"samples":
	   	{  
		  # Signal Region
                   "Zvv_signal"           :['signal','zjets',1,0]
                  ,"Zll_signal"           :['signal','zll',1,0]
                  ,"Wlv_signal"           :['signal','wjets',1,0]
                  ,"ttbar_signal"         :['signal','top',1,0]
                  ,"ST_signal"            :['signal','top',1,0]
                  ,"QCD_signal"           :['signal','qcd',1,0]
                  ,"Diboson_signal"       :['signal','diboson',1,0]
                  ,"Data_signal"          :['signal','data',0,0]
                                     
                  # Single muon-Control
                  ,"Wlv_singlemuon"        :['Wmn','wjets',1,1]
                  ,"Zll_singlemuon"        :['Wmn','zll',1,0]
                  ,"ttbar_singlemuon"      :['Wmn','top',1,0]
                  ,"ST_singlemuon"         :['Wmn','top',1,0]
                  ,"QCD_singlemuon"        :['Wmn','qcd',1,0]
                  ,"Diboson_singlemuon"    :['Wmn','diboson',1,0]
                  ,"Data_singlemuon"       :['Wmn','data',0,0]

                  # Single electron-Control
                  ,"Wlv_singleelectron"    :['Wen','wjets',1,1]
                  ,"Zll_singleelectron"    :['Wen','zll',1,0]
                  ,"ttbar_singleelectron"  :['Wen','top',1,0]
                  ,"ST_singleelectron"     :['Wen','top',1,0]
                  ,"QCD_singleelectron"    :['Wen','qcd',1,0]
                  ,"Diboson_singleelectron":['Wen','diboson',1,0]
                  ,"Data_singleelectron"   :['Wen','data',0,0]


                  # Double muon-Control	
                  ,"Zll_doublemuon"        :['Zmm','zll',1,1]
                  ,"ttbar_doublemuon"      :['Zmm','top',1,0]
                  ,"ST_doublemuon"         :['Zmm','top',1,0]
                  ,"QCD_doublemuon"        :['Zmm','qcd',1,0]
                  ,"Diboson_doublemuon"    :['Zmm','diboson',1,0]
                  ,"Data_doublemuon"       :['Zmm','data',0,0]

                  # Double electron-Control
                  ,"Zll_doubleelectron"    :['Zee','zll',1,1]
                  ,"ttbar_doubleelectron"  :['Zee','top',1,0]
                  ,"ST_doubleelectron"     :['Zee','top',1,0]
                  ,"QCD_doubleelectron"    :['Zee','qcd',1,0]
                  ,"Diboson_doubleelectron":['Zee','diboson',1,0]
                  ,"Data_doubleelectron"   :['Zee','data',0,0]

                  # Gamma + Jets
                  ,"GJets_photon"         :['Gjets','gjets',1,1]
                  ,"data_photon"          :['Gjets','data',0,0]

   	},
}

categories = [monojet_category]
