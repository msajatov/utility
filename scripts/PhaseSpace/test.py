from common.NN.ConfigParser import ConfigParser
import os

def main():
    
    filepath = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/dev/utility"
        
    era = "2017"
    channel = "mt"
    
    configpath = os.path.join(filepath, "config/samples/emb_frac_config_{0}_{1}.json".format(channel, era))
    
    parser = ConfigParser("mt", 2017, configpath)
    
    sample_sets = [sset for sset in parser.sample_sets if (not "_full" in sset.name)]
    sample_sets = [sset for sset in sample_sets if (not "AR" in sset.name)]
    
    for sset in sample_sets:
        print sset
        
    

if __name__ == '__main__':
    main()