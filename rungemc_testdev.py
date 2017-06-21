import os, subprocess, time, signal
from pathlib import Path

import os.path

def rungemc():
    #location of test experiment
    loc_directory = "/home/smarky/Desktop/clas12Tags-master/4a.1.0"

    #change the directory to the working directory
    os.chdir(loc_directory)

    #run gemc for test scenario
    p = subprocess.Popen(args=['/bin/csh', '-c', "gemc clas12.gcard -USE_GUI=0"])

    #check to see if gemc is done and exit when it is
    while True:
        if os.path.isfile("/home/smarky/Desktop/clas12Tags-master/4a.1.0/out.ev"):
            break
        else:
            pass

    #kill gemc amd subprocess
    os.system("pkill -HUP gemc");
    p.kill()

    #get the contents of the ouput file
    x = os.system("cat out.ev")

    return x
