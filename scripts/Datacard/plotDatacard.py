import common.PrettyPlotting as pl
from common.Tools.VarObject.VarObject import Var

import root_numpy as rn
import ROOT as R
from ROOT import TFile

import argparse
import os
import copy
import subprocess

def main():
    

    parser = argparse.ArgumentParser()
    parser.add_argument('var', nargs="+", help='Variable')
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt','et','tt'], default = 'mt')
    parser.add_argument('-o', dest='out', help='Path to outdir', default="" )
    parser.add_argument('-e', dest='era', help='Era',required = True )
    parser.add_argument('--real_est', dest='real_est', help='define which method to use for real part subtractio', choices = ['mc','frac'], default="mc" )
    parser.add_argument('--fake_est', dest='fake_est', help='define which method to use for determining fractions used in the fake factor method',
                        choices=['bin', 'nn'], default="bin")
    parser.add_argument('--syst', dest='syst', help='Add systematics and shape', action="store_true" )
    parser.add_argument('--debug', dest='debug', help='Debug Mode for FFs', action="store_true" )
    parser.add_argument('--plot_only', dest='plot_only', help='Plot datacard', action="store_true")
    parser.add_argument('--prefix', dest='prefix', help='Prefix for nn frac config', default="")
    parser.add_argument('-t', dest='type', help='Plot type')


    args = parser.parse_args()
#     Datacard.use_config = "conf" +  args.era

#     for u in args.var:
#         if args.out:
#             makePlot(args.channel, u, args.out, args.era, "{0}_{1}_plots".format(args.out, args.era))
#         else:
#             makePlot(args.channel, u, args.out, args.era)
        #input = raw_input("Enter any key to exit parent: ")
        
    indir = "/afs/cern.ch/work/m/msajatov/private/cms/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/shapes/emb_dc/{0}".format(args.out)
    dir = "/afs/cern.ch/work/m/msajatov/private/cms/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/shapes/emb_dc/{0}".format(args.out)
    for u in args.var:
        if args.syst:
            #indir = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest6/{0}/gof/2017/{1}/saturated/{2}".format(args.out, u, args.channel)
            #dir = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest6/{0}/gof/2017/{1}".format(args.out, u)
            indir = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fit_combination_corr/{0}/gof/2017/{1}/saturated/{2}".format(args.out, u, args.channel)
            dir = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fit_combination_corr/{0}/gof/2017/{1}".format(args.out, u)
        makePlot(args.channel, u, indir, args.era, dir, args, "{0}_{1}_plots".format(args.out, args.era), args.syst)

def makePlot(channel, variable, indir, era, dir, args, outdir = "", syst=False ):
    var = Var(variable)

    overlay = True
    plottype = args.type
    if plottype == "postfit":
        plottype = "postfit_sb"

    if "2016" in era: lumi = "35.9"
    if "2017" in era: lumi = "41.5"
    
    print "indir: {0}".format(indir)
    print "outdir: {0}".format(outdir)

    if indir and syst:  
        root_datacard = "/".join([indir, "2017_datacard_shapes_{0}.root".format(plottype) ])
    elif indir:
        root_datacard = "/".join([indir, "htt_{0}.inputs-sm-Run{1}-{2}.root".format(channel, era,var.name) ])
    else:
        root_datacard = "{0}/htt_{1}.inputs-sm-Run{2}-{3}.root".format("_".join([era, "datacards"]), channel, era, var.name)
    file = R.TFile(root_datacard)

    for category in file.GetListOfKeys():
        cat = category.GetName()
        interesting_ones = {}
        for h in ["W","VVT","VVL","VVJ","TTT","TTL","TTJ","ZTT","ZL","ZJ", "QCD",
                 "jetFakes","jetFakes_W","jetFakes_TT","jetFakes_QCD","EMB","data_obs", "ggH", "qqH"]:

            if h == "data_obs":
                interesting_ones["data"] = copy.deepcopy( file.Get("{0}/{1}".format(cat,h) ) )
            else:
                interesting_ones[h] = copy.deepcopy( file.Get("{0}/{1}".format(cat,h)  ) )
        

        plots = [ ("_def",["W","VVT","VVL","VVJ","TTT","TTL","TTJ","ZTT","ZL","ZJ","QCD","data"]),
                  ("_def_EMB",["W","VVL","VVJ","TTL","TTJ","EMB","ZL","ZJ","QCD","data"]),
                  ("_ff",["VVT","VVL","TTT","TTL","ZTT","ZL","jetFakes","data"]),
                  ("_ff_split",["VVT","VVL","TTT","TTL","ZTT","ZL","jetFakes_W","jetFakes_TT","jetFakes_QCD","data"]),
                  ("_ff_EMB_split",["VVL","TTL","ZL","EMB","jetFakes_W","jetFakes_TT","jetFakes_QCD","ggH","qqH","data"]),
                  ("_ff_EMB",["VVL","TTL","EMB","ZL","jetFakes","ggH","qqH","data"])
        ]
        
        print "indir: {0}".format(indir)
        print "outdir: {0}".format(outdir)
        
        for p in plots:
            histos = {}
            plot = True
            for h in p[1]:
                if type(interesting_ones[h]) == R.TObject: plot = False
                histos[h] = interesting_ones[h]
            if not outdir:
                outdir = "_".join([era, "plots/"])

            if plot and overlay: 
                textlines = collect(dir, args, plottype)
                pl.plot(histos, canvas="linear", signal = [], descriptions = {"plottype": "ProjectWork", "xaxis":var.tex, "channel":channel,"CoM": "13", "lumi":lumi  }, outfile = outdir +"/"+ cat+"_"+var.name + p[0] +".png", era=era, overlay=textlines )
            elif plot:
                pl.plot(histos, canvas="linear", signal = [], descriptions = {"plottype": "ProjectWork", "xaxis":var.tex, "channel":channel,"CoM": "13", "lumi":lumi  }, outfile = outdir +"/"+ cat+"_"+var.name + p[0] +".png", era=era)
    file.Close() 
    

def collect(dir, args, plottype):

    cwd = os.getcwd()

    plottype = plottype
    conf = args.out

    path = "{0}/{1}/{2}".format(dir, "saturated", args.channel)
    os.chdir(path)    

    file_input = "grepoutput.log"
    
    hosts_process = subprocess.Popen(['grep','Best fit r',file_input], stdout= subprocess.PIPE)
    hosts_out, hosts_err = hosts_process.communicate()

    initial = hosts_out.strip()
    initial = initial.replace("(68% CL)", "")
    initial = initial.strip()

    split = initial.split("  ")
    best_fit_r_1 = split[0]
    best_fit_r_2 = split[1]

    p_values = {}

    for test in ["saturated", "KS", "AD"]:
        path = "{0}/{1}/{2}".format(dir, test, args.channel)
        os.chdir(path)    

        file_input = "gof.json"

        hosts_process = subprocess.Popen(['grep','"p":',file_input], stdout= subprocess.PIPE)
        hosts_out, hosts_err = hosts_process.communicate()

        p_values[test] = hosts_out.strip()
        p_values[test] = p_values[test].replace("\"p\":", "p_" + test)

    textlines = []

    textlines.append(conf)
    textlines.append(plottype)
    textlines.append(best_fit_r_1)
    textlines.append(best_fit_r_2)
    textlines.append(p_values["saturated"])
    textlines.append(p_values["KS"])
    textlines.append(p_values["AD"])

    print textlines

    os.chdir(cwd)

    return textlines

if __name__ == '__main__':
    main()
        