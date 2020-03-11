import common.PrettyPlotting as pl
from common.Tools.VarObject.VarObject import Var

import root_numpy as rn
import ROOT as R
from ROOT import TFile

import argparse
import os
import copy
import subprocess
import string

def main():    

    parser = argparse.ArgumentParser()
    parser.add_argument('var', nargs="+", help='Variable')
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt','et','tt'], default = 'mt')
    parser.add_argument('-o', dest='out', help='Path to outdir', default="" )
    parser.add_argument('-e', dest='era', help='Era',required = True )
    parser.add_argument('-t', dest='type', help='Type (prefit, postfit, stat)',required = True )

    args = parser.parse_args()

    u = args.var

    for u in args.var:
        if args.type == "prefit":
            indir = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest6/{0}/gof/2017/{1}/".format(args.out, u, args.channel)
        elif args.type == "postfit":
            indir = "/afs/cern.ch/work/m/msajatov/private/cms2/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/fittest6/{0}/gof/2017/{1}/".format(args.out, u, args.channel)
        elif args.type == "stat":
            indir = "/afs/cern.ch/work/m/msajatov/private/cms/CMSSW_8_1_0/src/CombineHarvester/HTTSM2017/shapes/emb_dc/{0}".format(args.out)   

        textlines = collect(indir, args)    

        writeText(textlines, args, u)
    


def collect(dir, args):

    cwd = os.getcwd()

    plottype = args.type
    conf = args.out

    path = "{0}/{1}/{2}".format(dir, "saturated", args.channel)
    os.chdir(path)    

    file_input = "grepoutput.log"
    
    hosts_process = subprocess.Popen(['grep','Best fit r',file_input], stdout= subprocess.PIPE)
    hosts_out, hosts_err = hosts_process.communicate()

    initial = hosts_out.strip()
    initial = initial.replace("(68% CL)", "")

    best_fit_r_1 = initial

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
    textlines.append(p_values["saturated"])
    textlines.append(p_values["KS"])
    textlines.append(p_values["AD"])

    print textlines

    os.chdir(cwd)

    return textlines

def writeText(textlines, args, var):

    in_file = "{0}_2017_plots/htt_{1}_100_Run2017_{2}_{3}_ff_EMB.png".format(args.out, args.channel, args.type, var)
    out_file = "{0}_2017_plots/new_htt_{1}_100_Run2017_{2}_{3}_ff_EMB.png".format(args.out, args.channel, args.type, var)

    arguments = ["convert", "-font", "arial", "-fill", "black", "-pointsize", "20"]

    y_coord = 300
    for line in textlines:
        arguments = arguments + ["-draw", "text 420,{1} '{0}'".format(line, y_coord)]
        y_coord = y_coord + 20

    arguments = arguments + [in_file, out_file]

    print arguments

    hosts_process = subprocess.Popen(arguments, stdout= subprocess.PIPE)
    hosts_out, hosts_err = hosts_process.communicate()

if __name__ == '__main__':
    main()