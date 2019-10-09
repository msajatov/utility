import os
import argparse

from common.NN.ConfigParser import ConfigParser
from common.NN.DataReader import DataReader
from common.FractionPlotter import FractionPlotter
from common.NN.Settings import Settings


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt', 'et', 'tt', 'em'], default='mt')
    parser.add_argument('-m', dest='model',   help='ML model to use', choices=['keras', 'xgb'],  default='keras')
    parser.add_argument('-t', dest='train',   help='Train new model', action='store_true')
    parser.add_argument('-s', dest='scaler',   help='Global data scaler', choices=['none', 'standard'], default='none')
    parser.add_argument('-p', dest='predict', help='Make prediction', action='store_true')
    parser.add_argument('-f', dest='fractions', help='Plot Fractions', action='store_true')
    parser.add_argument('-tf', dest='trainingFracplots', help='Plot Fractions for training samples', action='store_true')
    parser.add_argument('-d', dest='datacard', help='Datacard', action='store_true')
    parser.add_argument('-e', dest='era',  help='Era', choices=["2016", "2017"], required = True)
    parser.add_argument('-ext', dest='ext_input', help='Use alternative sample input path for making predictions', action='store_true')
    parser.add_argument('bin_vars', nargs="*", help='Bin variable for fraction plots or datacard', default=[])
    args = parser.parse_args()
    
    # parser.add_argument('var', nargs="+", help='Variable')

    print "---------------------------"
    print "Era: ", args.era
    print "Running over {0} samples".format(args.channel)
    print "---------------------------"
    
    print args.bin_vars
    
    if not args.bin_vars:
        args.bin_vars = [
                        "pt_1",
                        "pt_2",
                        "jpt_1",
                        "jpt_2",
                        "bpt_1",
                        "bpt_2",
                        "njets",
                        "nbtag",
                        "m_sv",
                        "mt_1",
                        "mt_2",
                        "pt_vis",
                        "pt_tt",
                        "mjj",
                        "jdeta",
                        "m_vis",
                        "dijetpt",
                        "met",
                        "eta_1",
                        "eta_2"
                        ]
        
    print args.bin_vars

    run(args)


def run(args):

    channel = args.channel
    era = args.era
    fractions = args.fractions
    bin_vars = args.bin_vars
    
    filepath = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/dev/utility"
        
    era = args.era
    channel = args.channel
    
    configpath = os.path.join(filepath, "config/samples/frac_config_{0}_{1}.json".format(channel, era))
    
    parser = ConfigParser(channel, era, configpath)
    
    settings = Settings(channel, era, "keras", "none")
    settings.config_parser = parser
    
    plotter = FractionPlotter(settings)

    train_sample_sets = [sset for sset in parser.samples if (not "_full" in sset.name)]
    train_sample_sets = [sset for sset in train_sample_sets if (not "AR" in sset.name)]

    ar_sample_sets = [sset for sset in parser.samples if "data_AR" in sset.name]

    complete_sample_sets = []
    complete_sample_sets += train_sample_sets
    complete_sample_sets += ar_sample_sets

    settings.filtered_samples = complete_sample_sets
    
    prediction_input_path = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/dev/nnFractions/output/predictions/4cat_vars6/2017"
    
    for sample in complete_sample_sets:
        sample.full_path = os.path.join(prediction_input_path, sample.source_file_name)

    outdirpath = "output"
    try:
        if not os.path.exists(outdirpath):
            os.makedirs(outdirpath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


    for variable in bin_vars:
        label_0 = r"N_{jet} = 0"
        label_1 = r"N_{jet} = 1"
        label_n = r"N_{jet} > 1"
        ##plotter.make_fraction_plots(ar_sample_sets, variable, "AR_njet_0", outdirpath, selection=" && njets == 0", ylabel="Background Fractions ({0})".format(label_0))  
        #plotter.make_fraction_plots(ar_sample_sets, variable, "AR_njet_1", outdirpath, selection=" && njets == 1", ylabel="Background Fractions ({0})".format(label_1)) 
        #plotter.make_fraction_plots(ar_sample_sets, variable, "AR_njet_n", outdirpath, selection=" && njets > 1", ylabel="Background Fractions ({0})".format(label_n)) 
        plotter.make_fraction_plots(ar_sample_sets, variable, "AR_inclusive", outdirpath, ylabel="Background Fractions")       


if __name__ == '__main__':
    main()
