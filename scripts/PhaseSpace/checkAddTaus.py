from common.NN.ConfigParser import ConfigParser
from common.NN.DataReader import DataReader

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
    
    configpath = os.path.join(filepath, "config/samples/emb_frac_config_{0}_{1}.json".format(channel, era))
    
    parser = ConfigParser(channel, era, configpath)
    
    samples = [sset for sset in parser.samples if (not "_full" in sset.name)]
    samples = [sset for sset in samples if (not "AR" in sset.name)]
    
    data = [sset for sset in parser.samples if "data_AR" in sset.name]
    
    reader = DataReader()
    df = reader.get_data_for_sample(sset, ["addtau_q", "pt_1"])
    print df   
    
    df.loc[:, 'addtau_q_1'] = df.A.map(lambda x: x[0])
    
    newdf = df[df[]]
        

if __name__ == '__main__':
    main()