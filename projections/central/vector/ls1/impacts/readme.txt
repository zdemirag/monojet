#few lines to run impacts in a parallelized way:

text2workspace.py monojet_vector.txt
combineTool.py -M Impacts -d monojet_vector.root -m 125 --doInitialFit --robustFit 1 -t -1 
combineTool.py -M Impacts -d monojet_vector.root -m 125 --robustFit 1 --doFits --rMin=-5 --rMax=5 -t -1 --job-mode lxbatch --task-name lxbatch-test --sub-opts='-q 1nh' --merge 2
combineTool.py -M Impacts -d monojet_vector.root -m 125 -o impacts.json -t -1
plotImpacts.py -i impacts.json -o impacts_asimov_vector


