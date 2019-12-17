import ROOT as R
import json
from array import array
import root_pandas as rp
import root_numpy as rn
from pandas import DataFrame,Series,concat
from common.Tools.CutObject.CutObject import Cut
from common.Tools.VarObject.VarObject import Var
from fractions_input import Era
import copy
import sys
import os
import math
import common.Plotting as pl
from make_fractions_workspace import compileWorkspace

R.gROOT.SetBatch(True)
R.gStyle.SetOptStat(0)

def main(raw_args=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt','et','tt','all'], default = 'mt')
    parser.add_argument('-p', dest='plot',    help='Plot fractions' , action = "store_true")
    parser.add_argument('-v', dest='visualize_only', help='Plot fractions only', action="store_true")
    parser.add_argument('-e', dest='era',    help='Era' , required=True)
    parser.add_argument('--var', dest='var', help='Bin var for 1D fraction plots', default='none')
    args = parser.parse_args()


    channels =[args.channel]
    if args.channel == "all": channels = ["et","mt","tt"]
    cut = "-MT- && -VETO- && -OS- && -TRIG-"

    subcuts = {
        "et":{ "incl": cut },
        "mt":{ "incl": cut },
        "tt":{ "incl": cut }    
    }

    if "pred" in args.era:
        subcuts["et"].update(
            {"cat0": " & ".join([ cut, "predicted_class == 0"]),
             "cat1": " & ".join([ cut, "predicted_class == 1"]),
             "cat2": " & ".join([ cut, "predicted_class == 2"]),
             "cat3": " & ".join([ cut, "predicted_class == 3"]),
             "cat4":   " & ".join([ cut, "predicted_class == 4"]),
             "cat5":  " & ".join([ cut, "predicted_class == 5"]),
             "cat6":  " & ".join([ cut, "predicted_class == 6"]),
             "cat7":" & ".join([ cut, "predicted_class == 7"])
            })
        subcuts["mt"].update(
            {"cat0": " & ".join([ cut, "predicted_class == 0"]),
             "cat1": " & ".join([ cut, "predicted_class == 1"]),
             "cat2": " & ".join([ cut, "predicted_class == 2"]),
             "cat3": " & ".join([ cut, "predicted_class == 3"]),
             "cat4":   " & ".join([ cut, "predicted_class == 4"]),
             "cat5":  " & ".join([ cut, "predicted_class == 5"]),
             "cat6":  " & ".join([ cut, "predicted_class == 6"]),
             "cat7":" & ".join([ cut, "predicted_class == 7"])
            })
        subcuts["tt"].update(
            {"cat0": " & ".join([ cut, "predicted_class == 0"]),
             "cat1": " & ".join([ cut, "predicted_class == 1"]),
             "cat2": " & ".join([ cut, "predicted_class == 2"]),
             "cat3": " & ".join([ cut, "predicted_class == 3"]),
             "cat4":   " & ".join([ cut, "predicted_class == 4"]),

            })

    bin_var = Var(args.var)

    for channel in channels:

        if args.var == 'none':
            
            # ANALYSIS
            # binned_in = ["pt_2","njets"]; binning =  [ (9, array("d",[20,30,35,40,45,50,80,90,100,200] ) ) , (3, array("d",[-0.5,0.5,1.5,15]) )  ]
            # binned_in = ["m_vis","njets"]; binning = [ (30,0,300 ) , (3, array("d",[-0.5,0.5,1.5,15]) )  ]
            # ---------------------------------------------------
            # binned_in = ["predicted_prob","eta_1"]; binning = [ (6,array("d",[0.125, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0])) , (1, array("d",[-5., 5.]) )  ]
            # binned_in = ["predicted_prob","njets"]; binning = [ (6,array("d",[0.125, 0.3, 0.4, 0.5, 0.6, 0.7, 1.0])) , (3, array("d",[-0.5,1.5,2.5,15]) )  ]
            # binned_in = ["m_vis","njets"];          binning = [ (11,array("d",[0,50,80,100,110,120,130,150,170,200,250,1000])) , (3, array("d",[-0.5,1.5,2.5,15]) )  ]
            binned_in = ["m_vis", "njets"];
            binning = [(30, 0, 300),
                       (1, array("d", [-0.5, 15]))]
        else:
            bin_var = Var(args.var)
            binned_in = [args.var, "njets"]
            binning = [bin_var.bins(), (1, array("d", [-0.5, 15]))]

        Frac = Fractions(channel, binned_in, binning , args.era )
        for name, sc in subcuts[channel].items():
            tmpcut = [ Cut( "-ANTIISO2- && " + sc, channel ) ]
            if channel == "tt":
                tmpcut.append( Cut( "-ANTIISO1- && " + sc, channel ) ) 

            Frac.cut = tmpcut

            if args.visualize_only:
                #Frac.visualize()
                Frac.visualizeNew(binned_in = binned_in)
                continue

            Frac.calc(outname = name )
            # Frac.calc()
            if args.plot:
                if args.var == 'none':
                    #Frac.visualize()
                    Frac.visualizeNew(binned_in = binned_in)
                else:
                    dir ="control_plots/{0}".format(args.era)
                    if not os.path.exists(dir):
                        os.makedirs(dir)
                    #Frac.visualize("", args.var, dir)
                    Frac.visualizeNew("", args.var, dir, binned_in = binned_in)

    if args.channel == "all":
        compileWorkspace( "{0}_preliminary_fractions".format( args.era  ), args.era, binned_in,
                          "{0}_preliminary_fractions/htt_ff_fractions_{0}.root".format( args.era  ) )
    
class Fractions():

    def __init__(self, channel, var, binning, era = "2017"):
        print "Era: ", era
        self.era = era
        self.channel = channel
        self.var = var
        self.binning = binning[0] + binning[1]

        
        fromEra = Era( era = era, channel = channel, shift = "NOMINAL" )
        
        self.lumi =        fromEra.lumi
        self.weights =     fromEra.weights
        self.tauidsfs =    fromEra.tauidsfs
        self.add_weights = fromEra.add_weights
        self.mcSamples =   fromEra.mcSamples
        self.dataSample =  fromEra.dataSample


        self.cut = [ Cut( "-ANTIISO2- && -MT- && -VETO- && -OS- && -TRIG- ", channel ) ]
        if channel == "tt":
            self.cut.append( Cut( "-ANTIISO1- && -MT- && -VETO- && -OS- && -TRIG- ", channel ) )

        self.composition = {
                "w":["W","VVJ","ZJ"],
                "tt":["TTJ"],
                "qcd":["QCD"],
                "dy":["ZJ"],
        } 
        if "emb" in era:
            self.composition["real"]=["EMB","ZL","TTL","VVL"]
        else:
            self.composition["real"]=["ZTT","ZL","TTT","TTL","VVT","VVL"]

    def cpHist(self, h, name,title="", reset = True):
        newHist = copy.deepcopy(h)
        if reset: newHist.Reset()
        newHist.SetName(name)
        if title:
            newHist.SetTitle(title)
        else:
            newHist.SetTitle(name)

        return newHist

    def calc(self, outname="fractions"):
        aiso = 2
        for cut in self.cut:
            self.calcFractions(cut, "{0}_aiso{1}_{2}.root".format(self.channel, aiso, outname ) )
            aiso -= 1


    def calcFractions(self, cut, outname):
        if not os.path.exists("preliminary_fractions"):
            os.makedirs( "preliminary_fractions" )

        histos = {}

        for sample,name,addcut in self.mcSamples:
            histos[name] = self.fillHisto( sample, cut + addcut, name)

        histos["data"]     = self.fillHisto( self.dataSample, cut, "data_obs", weight = False )

        dummy = self.cpHist( histos["data"], "dummy", ":".join( self.var ) )

        print "dummy Y bins:"
        print dummy.GetNbinsY()
        fracs = {}
        fracs_original = {}        

        for f in ["total"] + self.getOtherParts():
            fracs[f] = self.cpHist(dummy, f)
            fracs_original[f] = self.cpHist(dummy, f)
 
        for i in xrange(1, dummy.GetNbinsX() + 1 ):
            for j in xrange(1, dummy.GetNbinsY() + 1 ):

                total = float( histos["data"].GetBinContent( i,j ) )
                part_mc = 0.
                part_other = {}
                for f in fracs:
                    if f == "total" or f == "QCD": continue

                    part_other[f] = max(0,histos[f].GetBinContent( i,j ) )
                    part_mc      += max(0,histos[f].GetBinContent( i,j ) )

                total = max(part_mc, total)
                part_other["QCD"] = total - part_mc

                for f in fracs:
                    if total == 0: continue
                    if f == "total":
                        fracs[f].SetBinContent( i,j, total )
                        fracs_original[f].SetBinContent( i,j, total )
                    else:
                        fracs[f].SetBinContent( i,j, part_other[f] / total )
                        fracs_original[f].SetBinContent( i,j, part_other[f] )

        comp = {}
        comp_original = {}
        for c,part in self.composition.items() :

            for i,p in enumerate( part ):
                if i == 0:
                    comp[c] = self.cpHist( fracs[p], c, reset = False)
                    comp_original[c] = self.cpHist( fracs_original[p], c, reset = False)
                else:
                    comp[c].Add( fracs[p] )
                    comp_original[c].Add( fracs_original[p] )

        if not os.path.exists(self.era + "_preliminary_fractions"):
            os.mkdir(self.era + "_preliminary_fractions")
        file = R.TFile(self.era + "_preliminary_fractions/{0}".format( outname ), "recreate" )
        
        file.mkdir("all")
        file.mkdir("fracs")
        file.mkdir("all_original")
        file.mkdir("fracs_original")
        file.cd()
        dummy.Write()

        file.cd("all")
        for f in fracs:
            fracs[f].Write()

        file.cd("fracs")
        for c in comp:
            comp[c].Write()  

        file.cd("all_original")
        for f in fracs_original:
            fracs_original[f].Write()

        file.cd("fracs_original")
        for c in comp_original:
            comp_original[c].Write()    

        file.Close()

        print "written fractions to:", self.era + "_preliminary_fractions/{0}".format( outname )

    def fillHisto(self, path, cut, name, weight = True):

        apply_cut = cut.get()
        if "EMB" in path:
            # use weight instead of emb_weight (this is important!)
            add_weights = ["weight"]
            weights = "weight"

        else:
            add_weights = self.add_weights
            weights = "*".join([self.weights, str(self.lumi) ])

            if "byTight" in apply_cut: tsf =  self.tauidsfs["tight"]
            if "byVTight" in apply_cut: tsf = self.tauidsfs["vtight"]

            weights += "*( (gen_match_2 != 5) + {0}*(gen_match_2 == 5) )"
            if self.channel == "tt":
                weights += "*( (gen_match_1 != 5) + {0}*(gen_match_1 == 5) )" 

            weights = weights.format(tsf)           

        tmpHist = R.TH2D(name,name,*( self.binning ))

        if not os.path.exists(path):
            print "Warning", path
            return tmpHist


        tmp =   rp.read_root( paths = path,
                              where = apply_cut,
                              columns = add_weights + self.var+ ["gen_match_1","gen_match_2","decayMode_1","decayMode_2","pt_2"] 
                            )

        if weight:
            
            tmp.eval( "eweight = " + weights ,  inplace = True )
            
        else:        
            tmp.eval( "eweight = 1"  , inplace = True )

        #dictionary
        tmpHist.SetOption("COLZ")
        rn.fill_hist( tmpHist, array = tmp[self.var].values,
                               weights = tmp["eweight"].values )

        return tmpHist

    def getOtherParts(self):

        otherParts = []
        for _, parts in self.composition.items():
            otherParts += parts

        return list(set(otherParts))

    def visualize_old(self, frac_file = "", outname = "", outdir=""):

        # contr = ["TT","W","QCD","real"]
        contr = ["tt", "w", "qcd", "real"]
        # contr = ["tt", "w", "qcd"]
        # if self.channel == "tt":
        #     contr.append("DY")


        # file = R.TFile( self.era + "_preliminary_fractions/{0}_aiso2_fractions.root".format( self.channel ), "read" )
        file = R.TFile(self.era + "_preliminary_fractions/{0}_aiso2_incl.root".format(self.channel), "read")


        Hists = { c:file.Get("fracs/"+c) for c in contr   }

        for i in xrange(1, Hists[ contr[0] ].GetNbinsY() + 1 ):

            hists = { c: Hists[c].ProjectionX(c +"x",i,i) for c in Hists }
            dummy = self.cpHist(hists[ contr[0] ], "Fractions")
            stack = R.THStack("stack", "")
            leg = R.TLegend(0.82, 0.5, 0.98, 0.9)
            for c in contr: 
                pl.applyHistStyle( hists[c], c )
                stack.Add( hists[c] )

            for c in contr[::-1]:
                leg.AddEntry( hists[c], c )

            cv = R.TCanvas(str(i)+"cv", str(i)+"cv", 10, 10, 700, 600)
            R.gPad.SetRightMargin(0.2)
            dummy.GetYaxis().SetRangeUser(0,stack.GetMaximum())
            dummy.Draw()
            stack.Draw("same")
            leg.Draw()
            R.gPad.RedrawAxis()

            outfile = os.path.join(outdir, str(i) + '_' +outname+ '_' +self.channel + '_fractions.png')
            cv.Print(outfile)

            cv.SaveAs(outfile.replace(".png", ".root"))

        file.Close()

    def visualizeNew(self, frac_file = "", outname = "", outdir="", binned_in=[]):

        contr = ["tt", "w", "qcd", "real"]
        input_frac_dir = "fracs_original/"
        plot_name = "frac"
        self.make_plot(contr, plot_name, outdir, input_frac_dir, binned_in)

        contr = ["tt", "w", "qcd", "real"]
        input_frac_dir = "fracs/"
        plot_name = "frac_norm"
        self.make_plot(contr, plot_name, outdir, input_frac_dir, binned_in)
        
        contr = self.composition["w"] + self.composition["tt"] + self.composition["qcd"] + self.composition["real"]
        input_frac_dir = "all_original/"
        plot_name = "all"
        self.make_plot(contr, plot_name, outdir, input_frac_dir, binned_in)
        
        contr = self.composition["w"] + self.composition["tt"] + self.composition["qcd"] + self.composition["real"]
        input_frac_dir = "all/"
        plot_name = "all_norm"
        self.make_plot(contr, plot_name, outdir, input_frac_dir, binned_in)


    def make_plot(self, contr=[], outname = "", outdir="", input_frac_dir="", binned_in=[]):

        file = R.TFile(self.era + "_preliminary_fractions/{0}_aiso2_incl.root".format(self.channel), "read")
        
        Hists = { c:file.Get(input_frac_dir+c) for c in contr   }

        if binned_in:
            var = Var(binned_in[0])

        for i in xrange(1, Hists[ contr[0] ].GetNbinsY() + 1 ):

            hists = { c: Hists[c].ProjectionX(c +"x",i,i) for c in Hists }

            outfile = os.path.join(outdir, str(i) + '_' + outname + '_' + self.channel + '_fractions.png')

            descriptions = {"plottype": "ProjectWork", "xaxis": var.tex, "channel": self.channel, "CoM": "13",
                        "lumi": "41.5", "title": "", "yaxis": "Background Composition"}

            sorted = sort_by_target_names(hists)
            print sorted

            pl.simple_plot(sorted, canvas="linear", signal=[],
                       descriptions=descriptions, outfile=outfile, optimizeTicks=True)

        file.Close()

def get_index_for_fraction_name(listitem):
    name = listitem[0]

    if name == "tt":
        print "name is tt"
        return 0
    elif name == "w":
        print "name is w"
        return 1
    elif name == "qcd":
        print "name is qcd"
        return 2
    elif name == "real":
        print "name is real"
        return 3
    else:
        print "name is something else:"
        print name
        return 4

def sort_by_target_names(histograms):

    print "histograms:"
    print histograms

    names = [(name, (name, h)) for name, h in histograms.items()]
    names.sort(key=get_index_for_fraction_name)
    sorted = [copy.deepcopy(n[1]) for n in names]

    return sorted

if __name__ == '__main__':
    main()
