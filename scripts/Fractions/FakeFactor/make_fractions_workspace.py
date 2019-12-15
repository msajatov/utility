#!/usr/bin/env python
import ROOT
import imp
import json
from array import array
wsptools = imp.load_source('wsptools', 'workspaceTools.py')


def GetFromTFile(str):
    f = ROOT.TFile(str.split(':')[0])
    obj = f.Get(str.split(':')[1]).Clone()
    f.Close()
    return obj

def generatePathToHistos(directory, channel, categories ):

    hists = []


    aiso = ["2"]
    if channel == "tt":
        aiso.append("1")        
    for category in categories:
        for frac in ["real","w","tt","qcd"]:
            for i in aiso:
                prefix = channel[0]
                if channel == "tt":
                    prefix += i

                hists.append( ( '{0}/{1}_aiso{2}_{3}.root:fracs/{4}'.format(directory, channel, i, category, frac), 
                                '{0}_{1}_frac_{2}'.format(prefix, category, frac)     ) )

    return hists

def compileWorkspace(directory, era, binned_in, outfile = "htt_ff_fractions.root"):
    # Boilerplate
    ROOT.PyConfig.IgnoreCommandLineOptions = True
    ROOT.gROOT.SetBatch(ROOT.kTRUE)
    ROOT.RooWorkspace.imp = getattr(ROOT.RooWorkspace, 'import')
    ROOT.TH1.AddDirectory(0)

    w = ROOT.RooWorkspace('w')

    if "pred" in era:
        mt_cat = ['incl','cat0','cat1','cat2','cat3','cat4','cat5','cat6','cat7']
        et_cat = ['incl','cat0','cat1','cat2','cat3','cat4','cat5','cat6','cat7']
        tt_cat = ['incl','cat0','cat1','cat2','cat3','cat4','cat4','cat4','cat4']

    else:
        mt_cat = ['incl']
        et_cat = ['incl']
        tt_cat = ['incl']

    histsToWrap = generatePathToHistos(directory, "mt", mt_cat )
    histsToWrap += generatePathToHistos(directory, "et", et_cat )
    histsToWrap += generatePathToHistos(directory, "tt", tt_cat )

    for task in histsToWrap:
        wsptools.SafeWrapHist(w, binned_in, GetFromTFile(task[0]), name=task[1])


    # for cat in ['incl','cat0','cat1','cat2','cat3','cat4']:
    for cat in tt_cat:
        for frac in ['real','tt','qcd','w']:    
            wsptools.MakeBinnedCategoryFuncMap(w, 'aiso', [1,2,1000],
                                               't_{0}_frac_{1}'.format(cat, frac), 
                                               ['t1_{0}_frac_{1}'.format(cat, frac), 't2_{0}_frac_{1}'.format(cat, frac)])



   
    for frac in ['real','tt','qcd','w']:


        mt_bins = [-1.5 + j for j in range( len(mt_cat) +1 ) ]
        wsptools.MakeBinnedCategoryFuncMap(w, 'cat', mt_bins,
                                           'm_frac_'+frac,
                                           [ "m_{0}_frac_{1}".format(c, frac) for c in mt_cat  ] )

        et_bins = [-1.5 + j for j in range( len(et_cat) +1 ) ]
        wsptools.MakeBinnedCategoryFuncMap(w, 'cat', et_bins,
                                           'e_frac_'+frac,
                                           [ "e_{0}_frac_{1}".format(c, frac) for c in et_cat  ] )

        tt_bins = [-1.5 + j for j in range( len(tt_cat) +1 ) ]
        wsptools.MakeBinnedCategoryFuncMap(w, 'cat', tt_bins,
                                           't_frac_{0}'.format(frac),
                                           [ "t_{0}_frac_{1}".format(c, frac) for c in tt_cat  ]  )  


    w.Print()
    print "Write to", outfile
    w.writeToFile(outfile)
    w.Delete()
    

if __name__ == '__main__':

    compileWorkspace("2016_pred_preliminary_fractions","2016_pred", ["predicted_prob","eta_1"], "2016_pred_preliminary_fractions/htt_ff_fractions_2016_pred.root")
    f = ROOT.TFile("2016_pred_preliminary_fractions/htt_ff_fractions_2016_pred.root")
    w = f.Get("w")
    f.Close()

    for i in [1,2]:
        for j in [-1,0,2,3,4,5,6,7]:
            w.var("predicted_prob").setVal( 0.9)
            w.var("eta_1").setVal( 0.1 )
            # w.var("aiso").setVal(i)
            w.var("cat").setVal(j)
            if j == -1:
                cat = "incl"
            else:
                cat = "cat"+str(j)
            print "MT", i,j,w.function("m_{0}_frac_qcd".format(cat)).getVal() == w.function("m_frac_qcd").getVal(), w.function("m_{0}_frac_w".format(cat) ).getVal() == w.function("m_frac_w").getVal()
            print "ET", i,j,w.function("e_{0}_frac_qcd".format(cat)).getVal() == w.function("e_frac_qcd").getVal(), w.function("e_{0}_frac_w".format(cat) ).getVal() == w.function("e_frac_w").getVal()
            if j < 5: print "TT", i,j,w.function("t1_{0}_frac_qcd".format(cat)).getVal() == w.function("t_frac_qcd").getVal(), w.function("t1_{0}_frac_w".format(cat)).getVal() == w.function("t_frac_w").getVal()

            # print "ET", i,j,w.function("e_frac_real").getVal(), w.function("e_frac_qcd").getVal(), w.function("e_frac_w").getVal(), w.function("e_frac_tt").getVal()
            # print "TT", i,j,w.function("t_frac_real").getVal(), w.function("t_frac_qcd").getVal(), w.function("t_frac_w").getVal(), w.function("t_frac_tt").getVal()
            # print "MT", i,j,w.function("m_frac_real").getVal(), w.function("m_frac_qcd").getVal(), w.function("m_frac_w").getVal(), w.function("m_frac_tt").getVal()

