
import os
import glob
import time

while True:
    for filename in sorted(glob.glob(os.path.join('*/*/*/', 'core.*'))):
        print "will remove", filename
        os.remove(filename)
    
    print "sleeping 10 seconds"
    time.sleep(10)
    
