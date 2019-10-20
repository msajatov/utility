from common.NN.ConfigParser import ConfigParser
from common.NN.DataReader import DataReader
from common.FractionPlotter import FractionPlotter
from common.NN.Settings import Settings

import root_numpy as rn
import ROOT as R
from ROOT import TFile

import argparse
import os
import copy

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt', 'et', 'tt'], default='mt')
    parser.add_argument('-e', dest='era',  help='Era', choices=["2016", "2017"], required = True)
    args = parser.parse_args()
    
    filepath = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/dev/utility"
        
    era = args.era
    channel = args.channel
    
    configpath = os.path.join(filepath, "config/samples/antiiso/frac_config_{0}_{1}.json".format(channel, era))
    
    parser = ConfigParser(channel, era, configpath)
    
    settings = Settings(channel, era, "keras", "none")
    settings.config_parser = parser
    
    samples = [sset for sset in parser.samples if (not "_full" in sset.name)]
    samples = [sset for sset in samples if (not "AR" in sset.name)]
    
    reader = DataReader()
    
    for sset in samples:
#         print sset
#         df = reader.get_data_for_sample(sset, ["pt_1", "pt_2", "iso_1", "iso_2"])
#         print df   
#         print sset.full_path
        tfile = reader.get_root_tree(sset)
        
        tree = tfile.TauCheck
        
        sset.cut = sset.cut.switchCutTo("-ANTIISO1-")
        
        print "{0} {1}: {2}".format(sset.name, sset.cut.original, tree.GetEntries(sset.cut.get()))
        

if __name__ == '__main__':
    main()