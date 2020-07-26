import globalVars

from common.NN.ConfigParser import ConfigParser
from common.NN.DataReader import DataReader
from common.NN.Settings import Settings

import root_numpy as rn
import ROOT as R
from ROOT import TFile

from common.Tools.CutObject.CutObject import Cut

import argparse
import os
import copy

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt', 'et', 'tt'], default='mt')
    parser.add_argument('-e', dest='era',  help='Era', choices=["2016", "2017"], required = True)
    args = parser.parse_args()
    
    #print globalVars.__UTILITY_ROOT_PATH__
    #filepath = "/afs/cern.ch/work/m/msajatov/private/CMSSW_9_4_0/src/dev/utility"
        
    era = args.era
    channel = args.channel
    
    configpath = os.path.join(globalVars.__UTILITY_ROOT_PATH__, "config/samples/frac_config_{0}_{1}.json".format(channel, era))    
    parser = ConfigParser(channel, era, configpath)
    
    settings = Settings(channel, era)
    settings.config_parser = parser
    
    # filter samples defined in frac_config_xx_xx.json
    samples = [sample for sample in parser.samples if ("data" in sample.name)]
    # samples = [sample for sample in samples if (not "data" in sample.name)]

    newcut = Cut("-OS- && -ANTIISO-", channel)
    print "Additional cuts to apply: {0}".format(newcut.original)
    print ""

    for sample in samples:
        sample.cut = sample.cut + newcut
    
    reader = DataReader()    

    subcuts_1 = []
    subcuts_2 = []

    #for i in [1,2,3,4,5,6]:
    #    subcuts_1 += [" & gen_match_1 == {0}".format(i)]
    #    subcuts_2 += [" & gen_match_2 == {0}".format(i)]

    subcuts_1 += [""]
    subcuts_2 += [""]
    
    for sample in samples:
        print sample

        tfile = reader.get_root_tree(sample)        
        tree = tfile.TauCheck
        
        tempstring = ""

        for sc1 in subcuts_1:
            for sc2 in subcuts_2:
                completecut = sample.cut.get() + sc1 + sc2
                completecutname = sample.cut.original + sc1 + sc2
                val = tree.GetEntries(completecut)
                tempstring += str(val) + ";"
            print tempstring
            tempstring = ""

        print ""
        

if __name__ == '__main__':
    main()