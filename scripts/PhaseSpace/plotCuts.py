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
    
    configpath = os.path.join(filepath, "config/samples/emb_frac_config_{0}_{1}.json".format(channel, era))
    
    parser = ConfigParser(channel, era, configpath)
    
    settings = Settings(channel, era, "keras", "none")
    settings.config_parser = parser
    
    samples = [sset for sset in parser.samples if (not "_full" in sset.name)]
    samples = [sset for sset in samples if (not "AR" in sset.name)]
    
    data = [sset for sset in parser.samples if "data_AR" in sset.name]
    test = [sset for sset in parser.samples if "QCD" in sset.name]
    
    reader = DataReader()
    
    for sset in [test[0]]:
        print sset
#         df = reader.get_data_for_sample(sset, ["pt_1", "pt_2", "iso_1", "iso_2"])
#         print df   
        print sset.full_path
        tfile = reader.get_root_tree(sset)
        
        tree = tfile.TauCheck
        
        basecut = sset.cut
        canvases = []
        
#         selection = basecut.get()
#         print basecut.original
#         canvases.append(R.TCanvas("ANTIISO - iso_1", "ANTIISO - iso_1"))
#         tree.Draw("iso_1", selection)
#         canvases.append(R.TCanvas("ANTIISO - iso_2", "ANTIISO - iso_2"))
#         tree.Draw("iso_2", selection)
#         canvases.append(R.TCanvas("ANTIISO - pt_1", "ANTIISO - pt_1"))
#         tree.Draw("pt_1", selection)
        
#         ss_cut = basecut.switchCutTo("-SS-")
#         selection = ss_cut.get()
#         print ss_cut.original
#         canvases.append(R.TCanvas("ANTIISO SS- iso_1", "ANTIISO SS- iso_1"))
#         tree.Draw("iso_1", selection)
#         canvases.append(R.TCanvas("ANTIISO SS- iso_2", "ANTIISO SS- iso_2"))
#         tree.Draw("iso_2", selection)
#         canvases.append(R.TCanvas("ANTIISO SS- pt_1", "ANTIISO SS- pt_1"))
#         tree.Draw("pt_1", selection)
        
        
#         antiiso1_cut = basecut.switchCutTo("-ANTIISO1-")
#         selection = antiiso1_cut.get()
#         print antiiso1_cut.original
#         canvases.append(R.TCanvas("ANTIISO1 - iso_1", "ANTIISO1 - iso_1"))
#         tree.Draw("iso_1", selection)
#         canvases.append(R.TCanvas("ANTIISO1 - iso_2", "ANTIISO1 - iso_2"))
#         tree.Draw("iso_2", selection)
#         canvases.append(R.TCanvas("ANTIISO1 - pt_1", "ANTIISO1 - pt_1"))
#         tree.Draw("pt_1", selection)
#         
#         
#         antiiso2_cut = basecut.switchCutTo("-ANTIISO2-")
#         selection = antiiso2_cut.get()
#         print antiiso2_cut.original
#         canvases.append(R.TCanvas("ANTIISO2 - iso_1", "ANTIISO2 - iso_1"))
#         tree.Draw("iso_1", selection)
#         canvases.append(R.TCanvas("ANTIISO2 - iso_2", "ANTIISO2 - iso_2"))
#         tree.Draw("iso_2", selection)
#         canvases.append(R.TCanvas("ANTIISO2 - pt_1", "ANTIISO2 - pt_1"))
#         tree.Draw("pt_1", selection)

#         plot(canvases, tree, ["pt_1:iso_1"], basecut.switchCutTo("-ANTIISO2-"), "ANTIISO2")
#         plot(canvases, tree, ["pt_2:iso_2"], basecut.switchCutTo("-ANTIISO2-"), "ANTIISO2")
#         plot(canvases, tree, ["pt_1:iso_2"], basecut.switchCutTo("-ANTIISO2-"), "ANTIISO2")
#         plot(canvases, tree, ["pt_2:iso_1"], basecut.switchCutTo("-ANTIISO2-"), "ANTIISO2")
        
#         plot(canvases, tree, ["pt_1:pt_2"], basecut.switchCutTo("-ANTIISO1-"), "ANTIISO2")
#         plot(canvases, tree, ["iso_1:iso_2"], basecut.switchCutTo("-ANTIISO2-"), "ANTIISO2")
#         plot(canvases, tree, ["iso_1:iso_2"], basecut.switchCutTo("-ANTIISO1-"), "ANTIISO1")
#         plot(canvases, tree, ["iso_1:iso_2"], basecut.switchCutTo("-ANTIISO-"), "ANTIISO")
#         title = "{0} - ANTIISO2".format(sset.name)
#         item = "iso_1"
#         selection = basecut.switchCutTo("-ANTIISO2-").get()
#         ccv = R.TCanvas("{0} - {1}".format(title, item), "{0} - {1}".format(title, item))
#         tree.Draw(item, selection)
        
#         plot(canvases, tree, ["iso_1"], basecut.switchCutTo("-ANTIISO2-"), "{0} - ANTIISO2".format(sset.name))
#         plot(canvases, tree, ["iso_2"], basecut.switchCutTo("-ANTIISO1-"), "{0} - ANTIISO1".format(sset.name))

#         stacks = []
        

#         stackPlot(canvases, stacks, tree, ["iso_2"], basecut.switchCutTo("-ANTIISO1-"), "ANTIISO1")
#         stackPlot(canvases, stacks, tree, ["iso_1"], basecut.switchCutTo("-ANTIISO2-"), "ANTIISO2", new=False)
        
#         stack = R.THStack("hs", "")
#         
#         R.TCanvas("{0} - {1}".format("title", "item"), "{0} - {1}".format("title", "item"))  
#         tree.Draw("iso_2", basecut.switchCutTo("-ANTIISO1-").get())
#         histo = R.gPad.GetPrimitive("htemp")
#         print "hrllo"
#         stack.Add(histo)
#         
#         R.TCanvas("{0} - {1}".format("title", "item"), "{0} - {1}".format("title", "item"))  
#         tree.Draw("iso_1", basecut.switchCutTo("-ANTIISO2-").get())
#         histo = R.gPad.GetPrimitive("htemp")
#         stack.Add(histo)
#         
#         R.TCanvas("{0} - {1}".format("title", "item"), "{0} - {1}".format("title", "item"))      
#         
#         stack.Draw("nostack")

        sset.cut = sset.cut.switchCutTo("-ANTIISO1-")
#         
        doStuff([sset], settings)
        
        x = raw_input("raw input")

def doStuff(samples, settings):

    plotter = FractionPlotter(settings)

    outdirpath = "output"
    try:
        if not os.path.exists(outdirpath):
            os.makedirs(outdirpath)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        
    print "making val_plots"

    plotter.make_val_plots(samples, "iso_2", "", outdirpath)
   
        
# def stackPlot(canvases, stack, tree, what, cut, title, new=True):
#     
#     selection = cut.get()
#     print cut.original 
#     
#     for item in what:
#         if new:
#             canvases.append(R.TCanvas("{0} - {1}".format(title, item), "{0} - {1}".format(title, item)))       
#         histo = R.TH1F("myh")
#         tree.Draw(item + ">>myh", selection + ">>myh", "goff")
# #         histo = R.gDirectory.Get("myh")
#         stack.Add(histo)
#         stack.Draw("nostack")
# #         canvases.append(R.TCanvas("{0} - {1}".format(title, item), "{0} - {1}".format(title, item)))        
# #         tree.Draw(item + ">>myh", selection + ">>myh", "goff")
# #         histo = R.gDirectory.Get("myh")
# #         stack.Add(histo)
# #         stack.Draw("nostack")

def stackPlot(canvases, stacks, tree, what, cut, title, new=True):
    
    selection = cut.get()
    print cut.original 
    
    for item in what:
        if new:
            stacks.append(R.THStack("hs", ""))
            canvases.append(R.TCanvas("{0} - {1}".format(title, item), "{0} - {1}".format(title, item)))      
        tree.Draw(item, selection)
        histo = R.gPad.GetPrimitive("htemp")
        stacks[0].Add(histo)
        stacks[0].Draw("nostack")
#         canvases.append(R.TCanvas("{0} - {1}".format(title, item), "{0} - {1}".format(title, item)))        
#         tree.Draw(item + ">>myh", selection + ">>myh", "goff")
#         histo = R.gDirectory.Get("myh")
#         stack.Add(histo)
#         stack.Draw("nostack")
        
        
def plot(canvases, tree, what, cut, title):
    
    selection = cut.get()
    print cut.original
    
    for item in what:
        print item
        canvases.append(R.TCanvas("{0} - {1}".format(title, item), "{0} - {1}".format(title, item)))
        tree.Draw(item, selection)
        

if __name__ == '__main__':
    main()