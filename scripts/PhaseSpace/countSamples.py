from common.NN.ConfigParser import ConfigParser
from common.NN.DataReader import DataReader
from common.FractionPlotter import FractionPlotter
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
    
    filepath = "/afs/cern.ch/work/m/msajatov/private/CMSSW_9_4_0/src/dev/utility"
        
    era = args.era
    channel = args.channel
    
    configpath = os.path.join(filepath, "config/samples/antiiso/frac_config_{0}_{1}.json".format(channel, era))
    
    parser = ConfigParser(channel, era, configpath)
    
    settings = Settings(channel, era, "keras", "none")
    settings.config_parser = parser
    
    samples = [sset for sset in parser.samples if ("_full" in sset.name)]
    samples = [sset for sset in samples if (not "data" in sset.name)]
    # samples = [sset for sset in samples if (not "EMB" in sset.name)]
    
    reader = DataReader()

    
    # if channel == "et":
    #     correct_id_1 = 3
    # elif channel == "mt":
    #     correct_id_1 = 4
    # else:
    #     correct_id_1 = 5

    # correct_id_2 = 5

    # subcuts_1 = ["", " & gen_match_1 == {0}".format(correct_id_1), " & gen_match_1 != {0}".format(correct_id_1)]
    # subcuts_2 = ["", " & gen_match_2 == {0}".format(correct_id_2), " & gen_match_2 != {0}".format(correct_id_2)]

    subcuts_1 = []
    subcuts_2 = []

    for i in [1,2,3,4,5,6]:
        subcuts_1 += [" & gen_match_1 == {0}".format(i)]
        subcuts_2 += [" & gen_match_2 == {0}".format(i)]

    subcuts_1 += [""]
    subcuts_2 += [""]
    
    for sset in samples:
        print sset
#         df = reader.get_data_for_sample(sset, ["pt_1", "pt_2", "iso_1", "iso_2"])
#         print df   
        print sset.full_path
        tfile = reader.get_root_tree(sset)
        
        tree = tfile.TauCheck
        
        #sset.cut = sset.cut.switchCutTo("-ANTIISO1-")

        #newcut = Cut("-OS- && -ISO-", channel)
        #sset.cut = sset.cut + newcut
        
        tempstring = ""

        for sc1 in subcuts_1:
            for sc2 in subcuts_2:
                completecut = sset.cut.get() + sc1 + sc2
                completecutname = sset.cut.original + sc1 + sc2
                #print "{0}; {1}:".format(sset.name, completecutname)
                val = tree.GetEntries(completecut)
                #print "Count: {0}".format(val)
                tempstring += str(val) + ";"
            print tempstring
            tempstring = ""
        

if __name__ == '__main__':
    main()