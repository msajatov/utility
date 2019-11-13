#!/usr/bin/python
#alternative:
#python ../../../../scripts/postFitPlotJetFakes.py --file=all_shapes_mttot.root --ratio --extra_pad=0.6 --no_signal --file_dir="htt_mt_8" --custom_x_range --x_axis_min=0 --x_axis_max 200 --ratio_range 0.8,1.2 --manual_blind --x_blind_min=100 --x_blind_max=4000  --outname theirs --mode prefit --log_x --log_y
import ROOT as R
import copy
import sys
import getopt
import os
import math
import CMS_lumi, tdrstyle
from array import array
from collections import OrderedDict

COL_STORE = []

official_plots=True
#official_plots=False

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
#CMS_lumi.lumi_13TeV = "12.9 fb^{-1}"
#CMS_lumi.lumi_13TeV = "27.9 fb^{-1}"
CMS_lumi.lumi_13TeV = "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = CMS_lumi.lumi_13TeV+" (13 TeV)" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
#CMS_lumi.lumiTextSize=0.687500
CMS_lumi.lumiTextSize*=0.055/0.045
#CMS_lumi.cmsTextSize*=2
#CMS_lumi.lumiTextSize*=2
#CMS_lumi.lumiTextOffset=-1.0
#CMS_lumi.relPosX = -0.040
#CMS_lumi.relPosY =  0.06

iPos = 11
iPeriod = 0

R.gROOT.SetBatch(True)
R.gStyle.SetOptStat(0)

histos_incl = []
histos_bkg_incl = []
histo_total_bkg_incl = None
histos_sig_incl = []
data_incl = None
histo_comp_incl = None
do_incl = False
do_fit = 'all'
binning = []

#histo_types_dict =  { 'ggH':0 , 'qqH':0 , 'W':1, 'W_rest':1 , 'ZTT':2, 'ZJ':3 , 'ZJ_rest':3, 'ZL': 3, 'TTT': 4, 'TTJ': 4, 'TTJ_rest':4, 'VVT': 1, 'VVJ': 1, 'VVJ_rest': 1, 'QCD': 5, 'jetFakes': 6}
#histo_labels_dict = { 0:'ggH/qqH' , 1:'Electroweak', 2:'Z#rightarrow #tau#tau', 3:'Z#rightarrow ee/#mu#mu', 4:'t#bar{t}', 5:'QCD', 6:'Misidentified #tau'}
histo_types_dict =  { 'ggH':0 , 
                     'qqH':0 , 
                     'W':4, 
                     'W_rest':4 , 
                     'ZTT':1, 
                     'ZJ':2 , 
                     'ZJ_rest':2, 
                     'ZL': 2, 
                     'TTT': 3, 
                     'TTJ': 3, 
                     'TTJ_rest':3, 
                     'VVT': 4, 
                     'VVJ': 4, 
                     'VVJ_rest': 4, 
                     'QCD': 5, 
                     'jetFakes': 6,
                     'EMB': 1,
                     'TTL': 3,
                     'VVL': 4}


histo_labels_dict = { 0:'ggH/qqH' , 
                     4:'Electroweak', 
                     1:'Z#rightarrow #tau#tau', 
                     2:'Z#rightarrow ee/#mu#mu', 
                     3:'t#bar{t}', 
                     5:'QCD', 
                     6:'Misidentified #tau'}

inv_histo_labels_dict = dict((v, k) for k, v in histo_labels_dict.items())

def main(argv):
    global histos_incl
    global histos_bkg_incl
    global histo_total_bkg_incl
    global histos_sig_incl
    global data_incl
    global histo_comp_incl
    global do_incl
    global do_fit
    global official_plots
    global histo_labels_dict
    global inv_histo_labels_dict

    input_file='cmb/125/htt_mt_1_13TeV_shapes.root'
    input_file_comp=None
#    useFF=0
    nameset='0'
    pl_vars = ["m_vis"]
    plottype=['png','pdf']
    mass='125'
    m_doLog=0
    m_doSignal=True
#    m_doInc=False
    blind_threshold=0.3

    helpline='PlotFit.py -i <inputfile> -m <mode> -n <nameset> -v <var> -p <plottype> -l <log> -b <blind>'
    try:
        opts, args = getopt.getopt(argv,"a:b:f:h:i:j:l:m:n:o:p:s:v:",["add=","blind=","ifile=","ifile_comp=","fit=","log=","mass=","name=","official_plots=","signal=","var=","plottype="])
    except getopt.GetoptError:
        print helpline
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print helpline
            print 'mode: 0 (default; standard methods), 1 (FF)'
            print 'plottype: png, eps, pdf etc'
            print 'blind: threshold. 0.3 default. Negative number for no blinding.'
            sys.exit()
        elif opt in ("-a", "--add"):
            do_incl=True
#            do_incl=False
        elif opt in ("-f", "--fit"):
            do_fit = arg
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-j", "--ifile_comp"):
            input_file_comp = arg
        elif opt in ("-v", "--var"):
            pl_vars = [ arg ]
        elif opt in ("-b", "--blind"):
            blind_threshold = float(arg)
        elif opt in ("-p", "--plottype"):
            plottype = arg.split(',')
            if 'png' in plottype:
                plottype.append(plottype.pop(plottype.index('png')))  #move to end of the list, needed to get transparency right
        elif opt in ("-m", "--mass"):
            mass = arg
#            histo_labels_dict[0]='H('+mass+')'
#            print 'YYY',mass,arg,histo_labels_dict[0]
#            inv_histo_labels_dict = dict((v, k) for k, v in histo_labels_dict.items())            
        elif opt in ("-o", "--official_plots"):
            if arg=='0': official_plots=False
            else: official_plots=True
        elif opt in ("-l", "--log"):
            m_doLog=int(arg)
        elif opt in ("-s", "--signal"):
            if arg=='0': m_doSignal=False
            else: m_doSignal=True
        elif opt in ("-n", "--nameset"):
            nameset=arg

    print 'Input file: ', input_file

    input_dir=os.path.split(input_file)[0]
    print 'Input dir : ', input_dir

#    print 'Using FF? ', useFF
    print 'Name set: ', nameset
    print 'plottype: ', plottype
    print 'mass: ', mass
    print 'postfit: ', do_fit
    print 'blind thrsh: ', blind_threshold
    print 'Var: ', pl_vars

    var_dict = {
        'm_vis-2D':'2D',
        'm_vis':'m_{vis} [GeV]',
        'm_sv-2D':'2D',
        'm_sv':'m_{sv} [GeV]',
        'pt_sv':'p_{T,sv} [GeV]',
        'met':'E^{miss}_{T} [GeV]',
        'pt_1':'p_{T}^{1} [GeV]',
        'pt_2':'p_{T}^{2} [GeV]',
        'eta_1':'#eta^{1} [GeV]',
        'eta_2':'#eta^{2} [GeV]',
        'mt_1':'m_{T}^{1} [GeV]',
        'mt_2':'m_{T}^{2} [GeV]',
        'mt_3':'m_{T}^{3} [GeV]',
        'mttot':'m_{T,tot} [GeV]',
        'Hpt':'p_{T}^{H} [GeV]',
        'mjj':'m_{jj} [GeV]',
        'ML':'ML score',
        }

    if official_plots:
        histo_dict =[ 
#            ('TotalSig','#phi_{700}, #sigma_{gg/bb}=0.1pb'),
            ('ggH','ggH'+mass),
            ('qqH','qqH'+mass),
            ('ZL','Z#rightarrow ee/#mu#mu'), 
            ('TTT','t#bar{t}, #tau#rightarrow#tau'),
            ('W','W'),
            ('VVT','VV, #tau#rightarrow#tau'),
            ('jetFakes','j#rightarrow#tau'),
            ('EMB', 'Z#rightarrow #tau#tau (emb)'),
            ('VVL', 'VVL'),
            ('TTL', 'TTL')
            ]
    else:
        histo_dict =[ 
            ('ggH','ggH'+mass),
            ('qqH','qqH'+mass),
            ('jetFakes','j#rightarrow#tau'),
            ('ZJ','Z#rightarrow ll, j#rightarrow#tau'), 
            ('ZL','Z#rightarrow ll, l#rightarrow#tau'), 
            ('TTT','t#bar{t}, #tau#rightarrow#tau'),
            ('VVT','VV, #tau#rightarrow#tau'),
            ('EMB', 'Z#rightarrow #tau#tau (emb)'),
            ('VVL', 'VVL'),
            ('TTL', 'TTL')
            ]

    histo_dict = OrderedDict(histo_dict)

    for i,pl_var in enumerate(pl_vars):
        root_file = input_file
        if not os.path.exists(root_file): continue
        tmp = R.TFile(root_file)

        folders=[]
        for key in tmp.GetListOfKeys(): #do only prefit, only postfit, or all
            if 'prefit' in key.GetTitle() and not do_fit=='post': folders.append( key.GetTitle() )
            elif 'postfit' in key.GetTitle() and not do_fit=='pre': folders.append( key.GetTitle() )
#        ncat=len(folders)

#        for key in tmp.GetListOfKeys():
#            if 'postfit' in key.GetTitle(): folders.append( key.GetTitle() )

##tg
#Because of rebinning: start with folder with minimum number of bins
#        folders[3], folders[0] = folders[0], folders[3]
        nbins_min=9999
        nbins_min_ind=-1
        for i, folder in enumerate(folders):
#            if not folder[7].isdigit(): continue
#            if int(folder[7])>=2 and int(folder[7])<=5: continue
#            if int(folder[7])==1: 
#                if not folder[8].isdigit() or int(folder[8])>3: continue

            f0 = R.TFile(root_file)
            h = copy.deepcopy( f0.Get('{0}/data_obs'.format(folder)) )
            nbins=h.GetNbinsX()
            if nbins_min>nbins:
                nbins_min=nbins
                nbins_min_ind=i

        folders[nbins_min_ind], folders[0] = folders[0], folders[nbins_min_ind]


#        for key in tmp.GetListOfKeys():
#            folder = key.GetTitle()
        incl_name=None
        for i, folder in enumerate(folders):
 #           if not folder[7].isdigit(): continue
 #           if int(folder[7])>=2 and int(folder[7])<=5: continue
 #           if int(folder[7])==1:
 #               if not folder[8].isdigit() or int(folder[8])>3: continue

            m_outname = getName(folder,input_dir)
            if not incl_name: incl_name=folder
            print 'root_file, folder, m_outname',root_file, folder, m_outname

#            histo_name_total_bkg = '{0}/TotalBkg'.format(folder)
            histo_name_total_bkg = 'TotalBkg'.format(folder)

            histo_types_names = [
                'SM H#to#tau#tau',                    #0
                'Z#to#tau#tau, e/#mu/#tau#to#tau',    #1
                'jet#to#tau misID',                   #2
                't#bar{t}, e/#mu/#tau#to#tau',        #3
                'VV, single-top',                     #4
                'multi-jet',                          #5
                ]
                
            m_infoleft = m_outname

            if 'htt_mt_' in m_outname: m_infoleft='#mu#tau '
            if 'htt_et_' in m_outname: m_infoleft='e#tau '
            if 'htt_tt_' in m_outname: m_infoleft='#tau#tau '

            if '_nobtag_' in m_outname: m_infoleft+='0 btag'
            if '_btag_' in m_outname: m_infoleft+='  btag'

            if not 'htt_tt_' in m_outname:
                if '_tight' in m_outname: m_infoleft+=', tight'
                if '_loosemt' in m_outname: m_infoleft+=', loose mT'

            m_title_x=var_dict[pl_var] if pl_var in var_dict else pl_var

            if 'htt_mt' in m_outname or 'htt_et' in m_outname:
                m_title_x=m_title_x.replace("m_{T}^{1}","m_{T}")
                m_title_x=m_title_x.replace("m_{T}^{2}","m_{T}(#tau+E_{T}^{miss})")
                m_title_x=m_title_x.replace("^{2}","^{#tau}")
                if 'htt_mt' in m_outname:
                    m_title_x=m_title_x.replace("^{1}","^{#mu}")
                if 'htt_et' in m_outname:
                    m_title_x=m_title_x.replace("^{1}","^{e}")
            if 'htt_tt' in m_outname:
                m_title_x=m_title_x.replace("^{1}","^{#tau,1}")
                m_title_x=m_title_x.replace("^{2}","^{#tau,2}")

            if input_file_comp:
                m_outname+='_comp'

            display = DisplayManager(
                outname = m_outname,
                datatype = plottype,
                ratio = True,
                Title_X = m_title_x,
                InfoLeft = m_infoleft,
                InfoRight = "",
                doLog = m_doLog
                )

            display.showSignal = m_doSignal
            display.SetData(root_file, '{0}/data_obs'.format(folder))

#            display.SetData(root_file, '{0}/data_obs'.format(folder))
            if input_file_comp: 
                display.SetData(input_file_comp, '{0}/TotalBkg'.format(folder), True)

            display.getAllHistos(root_file, folder, histo_dict, histo_types_dict, histo_name_total_bkg)

            if official_plots: 
                display.histos=display.mergeHistos(display.histos)
                display.histos_bkg=display.mergeHistos(display.histos_bkg)
            display.stackHistos(display.histos)
            display.stackHistos(display.histos_bkg)
            display.stackHistos(display.histos_sig)
            display.AddCMS = True
            display.AddInfoLeft = True
            display.AddInfoRight = False
            if blind_threshold>0:
                display.BlindData = True
                display.blind_threshold=blind_threshold
            display.UseTotalBkg = True
#            display.UseTotalBkg = False
#            display.titles = histo_dict
            display.histo_types = histo_types_dict

            xmin=None
            xmax=None
            if pl_var=='mt_1': xmax=70
            if pl_var=='nbtag': xmin,xmax=-0.5,5.0
            if pl_var=='ML': xmin,xmax=0.2000001,1.0

#            if False: #pl_var=='pt_1' or pl_var=='pt_2':
            if pl_var=='pt_1' or pl_var=='pt_2':
                if 'htt_tt'     in m_outname: xmin,xmax=40,120
                else:                         xmin,xmax=30,200

            display.Draw(xmin,xmax,histo_dict)

            ####inclusive
#            if not (i+1) % ncat:
#                if not do_incl: continue
        if do_incl:
            if '2D' in root_file: continue

            m_outname = getName(incl_name,input_dir,'incl')
            m_infoleft= m_outname

            if 'htt_em_' in m_infoleft: m_infoleft='e#mu'
            if 'htt_mt_' in m_infoleft: m_infoleft='#mu#tau'
            if 'htt_et_' in m_infoleft: m_infoleft='e#tau'
            if 'htt_tt_' in m_infoleft: m_infoleft='#tau#tau'

            if input_file_comp:
                m_outname+='_comp'

            display = DisplayManager(
                outname = m_outname,
                datatype = plottype,
                ratio = True,
                Title_X = m_title_x,
                InfoLeft = m_infoleft,
                InfoRight = "",
                doLog = m_doLog
                )
        
            display.showSignal = m_doSignal
            display.histos=histos_incl
            display.histos_bkg=histos_bkg_incl
            display.histos_sig=histos_sig_incl
            display.histo_total_bkg=histo_total_bkg_incl
            display.histo_comp=histo_comp_incl
            display.data=data_incl
            if official_plots:
                display.histos=display.mergeHistos(display.histos)
                display.histos_bkg=display.mergeHistos(display.histos_bkg)
            display.stackHistos(display.histos)
            display.stackHistos(display.histos_bkg)
            display.stackHistos(display.histos_sig)
            display.AddCMS = True
            display.AddInfoLeft = True
            display.AddInfoRight = False
            if blind_threshold>0:
                display.BlindData = True
                display.blind_threshold=blind_threshold
            display.UseTotalBkg = True

            display.histo_types = histo_types_dict
        
            display.Draw(xmin,xmax,histo_dict)

            histos_incl=[]
            histos_bkg_incl=[]
            histos_sig_incl=[]
            histo_total_bkg_incl=None
            data_incl=None



#   raw_input("Press Enter to end")

def getName(in_name,dirname,incl=False):

    out_name=in_name

    cats=[ 'ggH', 'qqH' , 'W' , 'ZTT' , 'tt', 'multi-jet', 'ZL' , 'sT-diboson']

    if incl:
        cats=[ 'inclusive', 'inclusive'   , 'inclusive' , 'inclusive' , 'inclusive' , 'inclusive' ]
        
    out_name = out_name.replace('_2_13TeV','_'+cats[0]+'_13TeV')
    out_name = out_name.replace('_3_13TeV','_'+cats[1]+'_13TeV')
    out_name = out_name.replace('_11_13TeV','_'+cats[2]+'_13TeV')
    out_name = out_name.replace('_12_13TeV','_'+cats[3]+'_13TeV')
    out_name = out_name.replace('_13_13TeV','_'+cats[4]+'_13TeV')
    out_name = out_name.replace('_14_13TeV','_'+cats[5]+'_13TeV')
    out_name = out_name.replace('_15_13TeV','_'+cats[6]+'_13TeV')
    out_name = out_name.replace('_16_13TeV','_'+cats[7]+'_13TeV')

    out_name = os.path.join(dirname, out_name)

    return out_name

def createRatioCanvas(name, errorBandFillColor=14, errorBandStyle=3354):

    H_ref = 600
    W_ref = 800 
    W = W_ref
    H  = H_ref

# references for TT, BB, LL, RR
    TT = 0.08*H_ref
    BB = 0.12*H_ref 
    LL = 0.12*W_ref
    RR = 0.04*W_ref

#    cv = R.TCanvas(name, name, 10, 10, 700, 600)
    cv = R.TCanvas(name,name,50,50,W,H)
 
   # this is the tricky part...
    # Divide with correct margins
    cv.Divide(1, 2, 0.0, 0.0)

    # Set Pad sizes
    cv.GetPad(1).SetPad(0.0, 0.32, 1., 1.0)
    cv.GetPad(2).SetPad(0.0, 0.00, 1., 0.34)

#    cv.GetPad(1).SetFillStyle(4000)
    cv.GetPad(2).SetFillStyle(4000) #needed!

    cv.SetFillColor(0)
    cv.SetBorderMode(0)
    cv.SetFrameFillStyle(0)
    cv.SetFrameBorderMode(0)
    cv.SetLeftMargin( LL/W )
    cv.SetRightMargin( RR/W )
    cv.SetTopMargin( TT/H )
    cv.SetBottomMargin( BB/H )
    cv.SetTickx(0)
    cv.SetTicky(0)



    # Set pad margins 1
    cv.cd(1)
    R.gPad.SetTopMargin(0.08)
    R.gPad.SetLeftMargin(0.12)
    R.gPad.SetBottomMargin(0.03)
    R.gPad.SetRightMargin(0.1)

#    R.gPad.SetLogy(True)

    # Set pad margins 2
    cv.cd(2)
    R.gPad.SetBottomMargin(0.35)
    R.gPad.SetLeftMargin(0.12)
    R.gPad.SetRightMargin(0.1)
    R.gPad.SetGridy()

##    bogyHist = R.TH1F("legendPseudoHist", "", 1, 1., 2.)
##    bogyHist.SetFillColor(errorBandFillColor)
##    bogyHist.SetFillStyle(errorBandStyle)
##    bogyHist.SetLineColor(0)

    cv.cd(1)
    return cv


class DisplayManager(object):

    def __init__(self,
                 outname = 'out',
                 datatype = ['png'],
                 ratio = True,
#                 ratio = False,
                 Title_X = "#eta_{j1} [GeV]",
                 InfoLeft = "#mu#tau inclusive",
                 InfoRight = "",
                 doLog = 0
                 ):

        if ratio:
            self.canvas = createRatioCanvas(outname)
        else:
            self.canvas = R.TCanvas(outname)

        self.name = outname
        self.datatype = datatype
        self.showSignal = True
        self.doLog = doLog
        self.draw_ratio = ratio
        self.histos = []
        self.histos_bkg = []
        self.histo_total_bkg = None
        self.histos_sig = []
        self.data = None
        self.histo_comp = None
        self.histo_types = dict()
#        self.titles = []
#        self.titles = dict()
        self.Title_X = Title_X
        self.Title_Y = "Events"
        if 'njet' in Title_X or 'nbtag' in Title_X:
            self.Title_Y = "Events"
        if '#eta' in Title_X:
            self.Title_Y = "Events / unit"
        self.AddCMS = True
        self.AddInfoRight = True
        self.AddInfoLeft = True
        self.BlindData = False
        self.blind_threshold = 0.3
        self.UseTotalBkg = True
        self.InfoLeft = InfoLeft
        self.InfoRight = InfoRight
        self.errorHist = None
        if ratio:
#            self.Legend = R.TLegend(0.68, 0.52, 0.93, 0.92)
#           self.Legend = R.TLegend(0.68, 0.42, 0.93, 0.92)
#            self.Legend = R.TLegend(0.68, 0.39, 0.93, 0.89)
#            self.Legend = R.TLegend(0.71, 0.56, 0.87, 0.89)
#            self.Legend = R.TLegend(0.65, 0.45, 0.87, 0.89)
            self.Legend = R.TLegend(0.70, 0.46, 0.92, 0.90)
        else:
            self.Legend = R.TLegend(0.73, 0.53, 0.98, 0.89)

        self.applyLegendSettings(self.Legend)

#        self.draw_ratioLegend = R.TLegend(0.15, 0.79, 0.5, 0.89)
#        self.applyLegendSettings(self.draw_ratioLegend)

        self.pullRange = 0.58
    def applyLegendSettings(self,leg):
        leg.SetBorderSize(0)
        leg.SetFillColor(10)
        leg.SetLineWidth(0)
        leg.SetFillStyle(0)
        if self.draw_ratio:
#           leg.SetTextSize(0.040)
            leg.SetTextSize(0.050)
        else:
            leg.SetTextSize(0.050)
#       leg.SetTextFont(12)

#    def getAllHistos(self,root_file ,histo_names,histo_types,histo_name_total_bkg=''):
    def getAllHistos(self,root_file,folder,histo_dict,histo_types_dict,histo_name_total_bkg=''):
        histos = []
        histos_bkg = []
        histos_sig = []
        histo_total_bkg = None

        global histos_incl
        global histos_bkg_incl
        global histo_total_bkg_incl
        global histos_sig_incl

        fin = R.TFile(root_file)

#        for name,type in zip(histo_dict,histo_types_dict):
        for name in histo_dict:
            tmp = self.getHisto( fin, folder, name )
#            print 'gAH:',name,histo_types_dict[name]
            if not tmp:
                continue

#FIXME            if isTGraph(tmp):
#FIXME                tmp=scale_by_width(tmp);
#FIXME            else:
#FIXME                tmp.Scale(1.0,'width') #!!!

#            print 'histo          : ',tmp.GetNbinsX(),tmp.GetBinLowEdge(tmp.GetNbinsX()+1),tmp.GetBinContent(tmp.GetNbinsX()),tmp.GetBinError(tmp.GetNbinsX()),tmp.ClassName()

            histos.append(tmp)

            if histo_types_dict[name]==0: histos_sig.append(copy.deepcopy(tmp))
            else:                         histos_bkg.append(copy.deepcopy(tmp))

        if self.UseTotalBkg:
            histo_total_bkg = self.getHisto( fin, folder, histo_name_total_bkg , True)

#FIXME            if isTGraph(histo_total_bkg):
#FIXME                histo_total_bkg=scale_by_width(histo_total_bkg);
#FIXME            else:
#FIXME                histo_total_bkg.Scale(1.0,'width') #!!!

#            print 'histo_total_bkgA ',histo_total_bkg.GetNbinsX(),histo_total_bkg.GetBinLowEdge(histo_total_bkg.GetNbinsX()+1),histo_total_bkg.GetBinContent(histo_total_bkg.GetNbinsX()),histo_total_bkg.GetBinError(histo_total_bkg.GetNbinsX()),histo_total_bkg.ClassName()

#        print "Number of signal / bkg histos:",len(histos_sig),len(histos_bkg)

        fin.Close()
        self.histos = histos
        self.histos_bkg = histos_bkg
        self.histo_total_bkg = histo_total_bkg
        self.histos_sig = histos_sig

        if not '-2D_shapes' in root_file and do_incl:
            if not histos_incl:
                histos_incl = copy.deepcopy(histos)
                histos_bkg_incl = copy.deepcopy(histos_bkg)
                histos_sig_incl = copy.deepcopy(histos_sig)
                histo_total_bkg_incl = copy.deepcopy(histo_total_bkg)
            else: #only works if they are always in correct order! To do: check
                for h_incl,h_this in zip(histos_incl,histos):         self.check_and_add(h_incl,h_this)
                for h_incl,h_this in zip(histos_bkg_incl,histos_bkg): self.check_and_add(h_incl,h_this)
                for h_incl,h_this in zip(histos_sig_incl,histos_sig): self.check_and_add(h_incl,h_this)
                self.check_and_add(histo_total_bkg_incl,histo_total_bkg)
#               for h_incl,h_this in zip(histos_incl,histos):         h_incl.Add(h_this)
#               for h_incl,h_this in zip(histos_bkg_incl,histos_bkg): h_incl.Add(h_this)
#               for h_incl,h_this in zip(histos_sig_incl,histos_sig): h_incl.Add(h_this)
#               histo_total_bkg_incl.Add(histo_total_bkg)

        return histos

    def check_and_add(self,h1,h2):
        global do_incl

        if same_binning(h1,h2):
            h1.Add(h2)
        else:
            h2_rebin=save_binning(h1,h2)
#            h1_rebin=save_binning(h2,h1)
            if h2_rebin==None:
                do_incl=False
                print "Not the same binning... giving up on producing an inclusive histogram",h1.GetName()
#                if h1_rebin==None:
#                    print "other way: no"
#                else:
#                    print "other way: yes"
            else:
                h1.Add(h2_rebin)

    def getHisto(self,fin,folder,name,asym=False):
        m_name=folder+'/'+name
        tmp = copy.deepcopy( fin.Get(m_name) )
        try:
            if isTH(tmp):
                return tmp
            elif isTGraph(tmp):
                return copy.deepcopy(graph_to_histo(tmp,asym))
        except ReferenceError:
            print "{0} does not exist".format(m_name)   #TODO: Make visible!
            return 0
#            sys.exit()

    def applySystematics(self,systList):
        for i, syst in enumerate(systList):
            if syst == 0.: continue
            for j in xrange(self.histos[i].GetNbinsX()+1):
                self.histos[i].SetBinError(j, math.sqrt( self.histos[i].GetBinError(j)**2 + syst**2))


    def SetData(self,root_file, name, comp=False):
        global data_incl
        global histo_comp_incl
        global binning

        f0 = R.TFile(root_file)
        h = copy.deepcopy( f0.Get(name) )
        if isTGraph(h):
            h = copy.deepcopy( graph_to_histo(h) )
        #do the following to get Poisson errors bars. does not work to just convert directly due to some bug, need to create a copy manually first

        ##tg
        # nbins=h.GetNbinsX()
        # xbins=[]

        # wbin=-1
        # wbin_last=-1
        # nonequi=False
        # for i in xrange(1,nbins+2):
        #     xbins+=[h.GetBinLowEdge(i)]
        #     if i>1:
        #         wbin=xbins[-1]-xbins[-2]
        #         if i>2 and not is_close(wbin,wbin_last): nonequi=True
        #     wbin_last=wbin
        

#         #the following distinction is not needed, using the variable width everywhere is fine
#         #   but: this produces a stupid root error message... hence keep the distinction
#         if nonequi: h2 = R.TH1F(h.GetName(),h.GetTitle(),nbins,array('d',xbins)) #for variable bin width
#         else:       h2 = R.TH1F(h.GetName(),h.GetTitle(),nbins,h.GetBinLowEdge(1),h.GetBinLowEdge(nbins+1)) #for fixed bin width

#         h2.SetBinErrorOption(R.TH1.kPoisson)
#         h2.SetDirectory(0)
#         for i in xrange(0,nbins+2): #include under/overflow
#             h2.SetBinContent(i,h.GetBinContent(i))
# #            print i,h2.GetBinContent(i),h2.GetBinErrorUp(i)
#         h2.SetBinErrorOption(R.TH1.kPoisson)
# #       self.data = h2    #for Poisson errors

#FIXME        if isTGraph(h): h=scale_by_width(h);
#FIXME        else: h.Scale(1.0,'width') #!!!

        if not '-2D_shapes' in root_file and do_incl:
            if not binning:
                binning = get_binning(h)
#                print 'BIN',binning,self.data.GetNbinsX()
            if not comp:
                if not data_incl: 
                    data_incl=copy.deepcopy(h)
                else:             
                    self.check_and_add(data_incl,h)
            else:
                if not histo_comp_incl: 
                    histo_comp_incl=copy.deepcopy(h)
                else:             
                    self.check_and_add(histo_comp_incl,h)

        if not comp: self.data = h    #for Gaussian errors
        else:        
            self.histo_comp = h
        f0.Close()


    def applyHistStyle(self, h):

        if official_plots:
            i_map=inv_histo_labels_dict
#                         Sig                             ZTT                             ZJ,ZL,Z_R                       TTT                             W,VVT,VVJ,VVJ_r
#                         QCD                             FF                              all else
            colours =  [  R.kWhite,                       R.TColor.GetColor(248,206,104), R.TColor.GetColor(100,192,232), R.TColor.GetColor(155,152,204), R.TColor.GetColor(222,90,106),
                          R.TColor.GetColor(250,202,255), R.TColor.GetColor(192,232,100), R.kPink+3 ] #official
#                         Sig                             W,VVT,VVJ,VVJ_r                 ZTT                            ZJ,ZL,Z_R                       TTT
#                         QCD                             FF                              all else
#            colours =  [  R.kWhite,                       R.TColor.GetColor(222,90,106),  R.TColor.GetColor(248,206,104), R.TColor.GetColor(100,192,232), R.TColor.GetColor(155,152,204),
#                          R.TColor.GetColor(250,202,255), R.TColor.GetColor(192,232,100), R.kPink+3 ] #official
            no_line = [ 'TTT' , 'VVT', 'VVJ', 'ZJ' ]
        else: #FIXME!
            i_map={ 'TotalSig':0 , 'W':1, 'W_rest':1 , 'ZTT':2, 'ZJ':3 , 'ZJ_rest':3, 'ZL': 4, 'TTT': 5, 'TTJ': 6, 'TTJ_rest':6, 'VVT': 7, 'VVJ': 8, 'VVJ_rest': 8, 'QCD': 9, 'jetFakes': 10}
#                         Sig        W          ZTT,W_R   ZJ,Z_R       ZL            TTT         TTJ,TTJ_R  VVT          VVJ,VVJ_r   QCD       FF             all else
            colours =  [  R.kWhite,  R.kBlue+1, R.kRed+1, R.kBlue+0  , R.kMagenta+1, R.kGreen+1, R.kBlue-1, R.kOrange+1, R.kBlue-2 , R.kBlue-3,R.kBlue+1  ,   R.kPink+1 ] #ours
            no_line = [ ]

        b=h.GetName()
        if b in i_map:
            i=i_map[b]
        else:
            print 'Warning: Cannot find histo style for',b
            lastone=0
            for i in i_map: 
                if lastone<i_map[i]: lastone=i_map[i]
            i=lastone+1

#        colours =  [  R.kWhite,  R.kBlue+1, R.kRed+1, R.kYellow+1, R.kMagenta+1, R.kGreen+1, R.kCyan+1, R.kOrange+1, R.kAzure+1, R.kGray,  R.kPink+1  ,   R.kPink+3 ] #our old one
        line_col = [  R.kBlue+1, R.kBlack,  R.kBlack, R.kBlack,    R.kBlack,     R.kBlack,   R.kBlack,  R.kBlack,    R.kBlack,   R.kBlack, R.kBlack   ,   R.kBlack  ]
        line_sty = [  2,         1,         1,        1,           1,            1,          1,         1,           1,          1,        1          ,   1         ]    
#        line_wid = [  3,         2,         2,        2,           2,            2,          2,         2,           2,          2,        2          ,   2         ]    

        lw=1 #2
        lc=line_col[i]
        if i==0: lw=1 #3
        if b in no_line: 
            lw=0 #cannot really set to 0 in root...
            lc=colours[i]

#        h.SetLineColor(line_col[i]) 
        h.SetLineColor(lc) 
        h.SetLineWidth(lw)
#        h.SetLineWidth(line_wid[i])
        h.SetLineStyle(line_sty[i])
        h.SetFillColor(colours[i])

        #all below -- important for upper plot:
        std_size=0.035
        std_offs=0.005
        if isTH(h): h.SetStats(False)
        h.GetYaxis().SetTitle(self.Title_Y)
#        print 'XX '+h.GetName()+"  "+str(h.GetYaxis().GetLabelSize())+' '+str(h.GetYaxis().GetLabelOffset())
        h.GetXaxis().SetTitle(self.Title_X)
        h.GetYaxis().SetTitleOffset(0.9);
        h.GetYaxis().SetTitleSize(std_size*2.0)
        h.GetYaxis().SetLabelSize(std_size*2.0) #1.6
        h.GetYaxis().SetLabelOffset(std_offs*2.0)

    def applyDataStyle(self, h):
        h.SetLineColor(1)
#TEST        h.SetMarkerStyle(8)
        h.SetMarkerStyle(20)
#        h.SetMarkerSize(0.8)
        h.SetLineWidth(2) #1
#       h.SetStats(False)
#       h.GetYaxis().SetTitle(self.Title_Y)

        #important for ratio plot and thus x axis:
        std_size=0.035
        std_offs=0.005
        h.GetXaxis().SetTitle(self.Title_X)
        h.GetYaxis().SetTitleOffset(0.9);
        h.GetYaxis().SetTitleSize(std_size*2.0)
        h.GetYaxis().SetLabelSize(std_size*2.0) #1.6
        h.GetYaxis().SetLabelOffset(std_offs*2.0)
        h.GetXaxis().SetTitleOffset(0.9);
        h.GetXaxis().SetTitleSize(std_size*2.0)
        h.GetXaxis().SetLabelSize(std_size*2.0) #1.6
        h.GetXaxis().SetLabelOffset(std_offs*2.0)

    def applyCompStyle(self, h):
        h.SetLineColor(R.kRed+1)
        h.SetMarkerColor(R.kRed+1)
        h.SetMarkerStyle(25)
        h.SetMarkerSize(1.3)
        h.SetLineWidth(1) #2

    def mergeHistos(self,histos):
        newHistos = []

        lastone=0
        for i in histo_types_dict:
            if lastone<histo_types_dict[i]: lastone=histo_types_dict[i]
        for i in range(lastone+1):
            newHistos.append(None)

        for i,h1 in enumerate(histos):
            if h1.GetName() in histo_types_dict:
                ind=histo_types_dict[h1.GetName()]
            else:
                print 'Warning: Cannot find histo type for',h1.GetName()
                return
            if not newHistos[ind]:
                newHistos[ind]=copy.deepcopy(h1)
                newHistos[ind].SetName(histo_labels_dict[ind])
            else:
                newHistos[ind].Add(h1)

        while None in newHistos: newHistos.remove(None) #remove empty entries, e.g. jetFakes for default
        return newHistos

    def stackHistos(self, histos):

        
        is_tg=isTGraph(histos[0])

        newHistos = []
        for i,h1 in enumerate(histos):
            newHistos.append(h1)
            for j, h2 in enumerate(histos):
                if j > i:
                    if is_tg:
                        newHistos[i]=tg_add(newHistos[i],h2)
                    else:
                        newHistos[i].Add(h2)
        histos = newHistos

##TODO!!!
    def getErrorHist(self, ratio=False):

#        hin=R.TH1F() #not needed!?
        if self.UseTotalBkg:
            if self.histo_total_bkg==None: print 'ERROR: histo_total_bkg does not exist (value: None)'
            hin=self.histo_total_bkg
        else:
            hin=self.histos_bkg[0]

#        print 'histo_total_bkg: ',hin.GetNbinsX(),hin.GetBinLowEdge(hin.GetNbinsX()+1),hin.GetBinContent(hin.GetNbinsX()),hin.GetBinError(hin.GetNbinsX()),hin.ClassName()

#        if isTH(hin): #not needed!?
#            nbins=hin.GetNbinsX()
#            xbins=[]
#            for i in xrange(1,nbins+2):
#                xbins+=[hin.GetBinLowEdge(i)]
#            htmp = R.TH1F('uncertain','',nbins,array('d',xbins)) #for variable bin width
#        else:
#            htmp=copy.deepcopy(hin)
        htmp=copy.deepcopy(hin)

#       htmp.SetFillColor(CreateTransparentColor(12,0.4))
        htmp.SetFillColorAlpha(12,0.4)
        htmp.SetLineColor(0)
        htmp.SetMarkerSize(0)
#png files require the following line; pdf require it to be commented out (do not ask)
#        htmp.SetFillStyle(2001) #this fill style does not even exist (?) but none/1001 gives white fill, 3001 dotted fill... this works, dunno why, for PNG *only*.
#        htmp.SetFillStyle(3001)

        if ratio: 
            htmp.SetName('uncertainRatio')
            if isTGraph(hin):
                for i in xrange(0,hin.GetN()):
                    if hin.GetY()[i] < 1e-8:
                        htmp.GetY()[i]=0
                        htmp.SetPointError( i, 0,0,0,0 )
                    else:
                        htmp.GetY()[i]=1
                        htmp.SetPointError( i, 0,0, hin.GetErrorYlow(i) / hin.GetY()[i] , hin.GetErrorYhigh(i) / hin.GetY()[i] )
            else:
                for i in xrange(1,hin.GetNbinsX()+1 ):
                    if hin.GetBinContent(i) < 1e-8:
                        htmp.SetBinContent( i, 0 )
                        htmp.SetBinError( i, 0 )
                    else:
                        htmp.SetBinContent( i, 1 )
                        htmp.SetBinError( i, hin.GetBinError(i) / hin.GetBinContent(i) )
            self.errorRatioHist = copy.deepcopy(htmp)
        else:
#            if isTH(htmp): #not needed!?
#                for i in xrange(1,nbins+1): #w/o under/overflow
#                    htmp.SetBinContent( i, hin.GetBinContent(i) )
#                htmp.SetBinError( i, hin.GetBinError(i) )
            self.errorHist = copy.deepcopy(htmp)

    def blindData(self):

        if len(self.histos_sig)<1 or len(self.histos_bkg)<1:
            print 'WARNING: Cannot apply blinding: need at least one signal, and one background sample'
            return


        is_tg=isTGraph(self.histos[0])

        sigSumHist = copy.deepcopy(self.histos_sig[0])
        bkgSumHist = copy.deepcopy(self.histos_bkg[0])

        if is_tg: 
            nbins = self.histos[0].GetN()+1
            for i in xrange(1,len(self.histos_sig)):
                sigSumHist=tg_add(sigSumHist,self.histos_sig[i])
            for i in xrange(1,len(self.histos_bkg)):
                bkgSumHist=tg_add(bkgSumHist,self.histos_bkg[i])
        else:
            nbins = self.histos[0].GetNbinsX()+1
            for i in xrange(1,len(self.histos_sig)):
                sigSumHist.Add(self.histos_sig[i])
            for i in xrange(1,len(self.histos_bkg)):
                bkgSumHist.Add(self.histos_bkg[i])



        for i in xrange(0,nbins):
            b=bkgSumHist.GetY()[i] if is_tg else  bkgSumHist.GetBinContent(i)
            s=sigSumHist.GetY()[i] if is_tg else  sigSumHist.GetBinContent(i)
##            if (b>1e-8 and s/math.sqrt(b)>0.1) or (b<1e-8 and s>1e-8):
#            if (b>1e-8 and s/math.sqrt(b)>0.3) or (b<1e-8 and s>1e-8):
#                self.data.SetBinContent(i,1e9)
#                self.data.SetBinError(i,0.0)

#            d=b+0.09*0.09*b*b
            d=b+0.05*0.05*b*b
#            if (d>1e-8 and s/math.sqrt(d)>0.30) or (d<1e-8 and s>1e-8): #was: 0.3 instead of 0.15

            bkg_center=bkgSumHist.GetX()[i] if is_tg else bkgSumHist.GetBinCenter(i)
#            print '????',bkg_center,self.blind_threshold
            if (self.blind_threshold<10) and ( (d>1e-8 and s/math.sqrt(d)>self.blind_threshold) or (d<1e-8 and s>1e-8) ) or (self.blind_threshold>=10) and ('mttot' in self.name or 'm_vis' in self.name) and (bkg_center>self.blind_threshold) or (self.blind_threshold>=10) and ('met' in self.name) and (bkg_center>2*self.blind_threshold):
##                print '!!!!',bkg_center
                if is_tg: 
                    self.data.GetY()[i]=1e9
                    self.data.SetPointError(i,0,0,0,0)
                else: 
                    self.data.SetBinContent(i,1e9)
                    self.data.SetBinError(i,0.0)

            # if (self.blind_threshold<10) and ( (d>1e-8 and s/math.sqrt(d)>self.blind_threshold) or (d<1e-8 and s>1e-8) ): #was: 0.3 instead of 0.15
            #     self.data.SetBinContent(i,1e9)
            #     self.data.SetBinError(i,0.0)
            # if (self.blind_threshold>=10) and ('mttot' in self.name or 'm_vis' in self.name) and (bkgSumHist.GetBinCenter(i)>self.blind_threshold):
            #     self.data.SetBinContent(i,1e9)
            #     self.data.SetBinError(i,0.0)
            # if (self.blind_threshold>=10) and ('met' in self.name) and (bkgSumHist.GetBinCenter(i)>2*self.blind_threshold):
            #     self.data.SetBinContent(i,1e9)
            #     self.data.SetBinError(i,0.0)



    def Draw(self, xmin=None,xmax=None, histo_dict=[]):

        ymin = 0
        if isTGraph(self.data): 
            ymax=R.TMath.MaxElement(self.data.GetN(),self.data.GetY())
            print 'NNN',ymax
        else: ymax = self.data.GetMaximum()

        if self.AddCMS:
            if self.draw_ratio:
                ymax *= 1.3
            else:
                ymax *= 1.2
        else:
            ymax *= 1.05

        if self.doLog%10==1:                    #1 or 10
            ymax*=10000
            if 'm_{T,tot}' in self.Title_X or 'm_{vis}' in self.Title_X:
                ymin=0.00001
            elif 'eta' in self.Title_X:
                ymin=40
                ymax/=10
            else:
                ymin=0.2
        else:
            ymax*=1.2
            
        if self.BlindData:
            self.blindData()

        self.Legend.Clear()
        self.applyDataStyle(self.data)
        self.Legend.AddEntry(self.data, 'Observed') 
        self.getErrorHist()

        if self.histo_comp:
            alt_lbl='FF method'
            for i in self.histos_bkg:
                if i.GetName()=='Misidentified #tau':
                    alt_lbl='Classic method'

            self.applyCompStyle(self.histo_comp)
            self.Legend.AddEntry(self.histo_comp, alt_lbl, 'p') 

        hs=self.histos if self.showSignal else self.histos_bkg
        
        for i, h in enumerate(hs):
            self.applyHistStyle(h)
            if official_plots: title = h.GetName()
            else:              title = histo_dict[h.GetName()]
 
            h.GetYaxis().SetRangeUser(ymin, ymax)

            m_xmin=xmin if xmin else h.GetXaxis().GetXmin()
            m_xmax=xmax if xmax else h.GetXaxis().GetXmax()
            if xmin or xmax:
                h.GetXaxis().SetRangeUser(m_xmin, m_xmax)

            if ( official_plots and inv_histo_labels_dict[h.GetName()]>0 ) or ( not official_plots and self.histo_types[h.GetName()]>0 ):
                self.Legend.AddEntry(h, title ,'f') #bkg
            else:
                self.Legend.AddEntry(h, title ,'l') #signal
               
            if i ==0:
                if isTGraph(h): h.Draw('ALP')
                else: h.Draw('HIST')

                if self.draw_ratio:
                    h.GetXaxis().SetTitle("")

                if self.AddInfoRight:
                    if self.draw_ratio:
                        infoRight = R.TLatex( 0.67, 0.93, self.InfoRight )
                    else:
                        infoRight = R.TLatex( 0.65, 0.91, self.InfoRight )
                    infoRight.SetNDC();
                    infoRight.SetTextSize(0.055);
                    infoRight.Draw()

                if self.AddInfoLeft:
                    if self.draw_ratio:
                        infoLeft = R.TLatex( 0.12, 0.93, self.InfoLeft )
                    else:
                        infoLeft = R.TLatex( 0.10, 0.91, self.InfoLeft )
                    infoLeft.SetNDC();
                    infoLeft.SetTextSize(0.055);
                    infoLeft.Draw()

            else:
                h.Draw('SAME HIST')

#        print '0000',R.gROOT.GetListOfColors().GetLast()
#        self.errorHist.SetFillColor(CreateTransparentColor(12,0.4))
#        print '1111',R.gROOT.GetListOfColors().GetLast()
        self.errorHist.Draw("same E2")

#        self.Legend.AddEntry(self.errorHist, 'Bkg uncertainty','f')
        if self.histo_comp:
            self.histo_comp.Draw('SAME E0 P X0')
        self.data.Draw('SAME E0 P')
        self.Legend.Draw()

        if self.AddCMS:
            CMS_lumi.CMS_lumi(self.canvas.cd(1), iPeriod, iPos)

        if self.doLog==1: 
            R.gPad.SetLogy(True)
        elif self.doLog==10: 
            R.gPad.SetLogx(True)
        elif self.doLog==11: 
            R.gPad.SetLogx(True)
            R.gPad.SetLogy(True)

#        self.draw_ratio=False
        if self.draw_ratio:
            self.canvas.cd(2)


            histPull = copy.deepcopy(self.data)
            if self.histo_comp:
                histPullComp = copy.deepcopy(self.histo_comp)
#            histBkg  = copy.deepcopy(self.histos[0])
#            histBkg=self.histos_bkg[0]

            if self.UseTotalBkg:
                if self.histo_total_bkg==None: print 'ERROR: histo_total_bkg does not exist (value: None)'
                histBkg=copy.deepcopy(self.histo_total_bkg)
            else:
                histBkg=copy.deepcopy(self.histos_bkg[0])

#            print 'XXX ', self.histo_total_bkg.Integral(-1,-1), self.histos_bkg[0].Integral(-1,-1)

            if xmin or xmax:
                histPull.GetXaxis().SetRangeUser(m_xmin, m_xmax)
            histPull.GetYaxis().SetNdivisions(4) #TEST!

            #ratio should only contain observation uncertainties; prediction unc. are already in the band
            if isTGraph(histBkg):
                nbins = histBkg.GetN()
                for i in xrange(0,nbins):
#                    histBkg.SetPointError(i,0,0,0,0)
                    histPull.GetY()[i]/=histBkg.GetY()[i]
                    histPull.SetPointError(i,0,0, histPull.GetErrorYlow(i)/histBkg.GetY()[i], histPull.GetErrorYhigh(i)/histBkg.GetY()[i])
            else:
                nbins = histBkg.GetNbinsX()+1
                for i in xrange(0,nbins):
                   histBkg.SetBinError(i,0)
                histPull.Divide(histBkg)

#            histPull.UseCurrentStyle()
#            histPullComp.UseCurrentStyle()

#            histPull.SetLineColor(self.data.GetLineColor())
#            histPull.SetMarkerColor(self.data.GetLineColor())
#            histPull.SetMarkerStyle(self.data.GetMarkerStyle())
#            histPull.SetMarkerSize(self.data.GetMarkerSize())
#            histPull.SetLineStyle(self.data.GetLineStyle())
#            histPull.SetLineWidth(self.data.GetLineWidth())
     
            histPull.GetYaxis().SetRangeUser(-self.pullRange + 1., self.pullRange + 1.)
            

            # defaultYtoPixel = 408.  # height in pixels of default canvas
            defaultYtoPixel = self.canvas.GetPad(1).YtoPixel(0.)
            pad2YtoPixel = float(self.canvas.GetPad(2).YtoPixel(0))
            pad2XaxisFactor = defaultYtoPixel / pad2YtoPixel #!! * 1.5

            histPull.GetXaxis().SetLabelSize(self.data.GetXaxis().GetLabelSize()*pad2XaxisFactor*1.0) #
            histPull.GetXaxis().SetLabelOffset(self.data.GetXaxis().GetLabelOffset()*pad2XaxisFactor) #
            histPull.GetXaxis().SetTitleSize(self.data.GetXaxis().GetTitleSize()*pad2XaxisFactor*1.2) #
            histPull.GetXaxis().SetTitleOffset(self.data.GetXaxis().GetTitleOffset()/pad2XaxisFactor*2.1) #1.8 0.9

            histPull.GetYaxis().SetLabelSize(self.data.GetYaxis().GetLabelSize()*pad2XaxisFactor*1.0) #
            histPull.GetYaxis().SetLabelOffset(self.data.GetYaxis().GetLabelOffset()*pad2XaxisFactor*0.3)
            histPull.GetYaxis().SetTitleSize(self.data.GetYaxis().GetTitleSize()*pad2XaxisFactor*1.1) #
            histPull.GetYaxis().SetTitleOffset(self.data.GetYaxis().GetTitleOffset()/pad2XaxisFactor*0.87) #0.9 1.2 0.4

            histPull.GetYaxis().CenterTitle()
            histPull.GetXaxis().SetTickLength(histPull.GetXaxis().GetTickLength()*pad2XaxisFactor)
            histPull.GetYaxis().SetNdivisions(306)

#            histPull.GetYaxis().SetTitle("Data/MC")
            histPull.GetYaxis().SetTitle("obs/exp")
            histPull.SetTitle('')

            if isTGraph(histPull): histPull.Draw('Ae')
            else: histPull.Draw('e')

            if self.histo_comp:
                histPullComp.Divide(histBkg)
                histPullComp.Draw("e same x0")

#            self.getErrorRatioHist()
            self.getErrorHist(True) #True: make ratio
#            print '000000',R.gROOT.GetListOfColors().GetLast()
#            self.errorHist.SetFillColor(CreateTransparentColor(12,0.4))
#            print '111111',R.gROOT.GetListOfColors().GetLast()
            self.errorRatioHist.Draw("same E2")

#            self.draw_ratioLegend.AddEntry(histPull, "MC")
#            self.draw_ratioLegend.Draw()

#            for i, h in enumerate(self.histos):
            for i, h in enumerate(hs):
                h.GetXaxis().SetLabelSize(0)

            if self.doLog>=10: 
                R.gPad.SetLogx(True)

            self.canvas.cd(1)

        R.gPad.Update()
        R.gPad.RedrawAxis()

#        gErrorIgnoreLevel = kPrint, kInfo, kWarning, kError, kBreak, kSysError, kFatal  -- 0, 1000, 2000, 3000, 4000, 5000, 6000
        oldlvl=R.gErrorIgnoreLevel
        R.gErrorIgnoreLevel = R.kWarning
        for d in self.datatype:
            if d=='png':
                self.canvas.cd(1)
                self.errorHist.SetFillStyle(2001)
                if self.draw_ratio:
                    self.canvas.cd(2)
                    self.errorRatioHist.SetFillStyle(2001)
            self.canvas.Print( '.'.join([self.name, d]))
            #self.canvas.SaveAs( '.'.join([self.name, 'C']))
        R.gErrorIgnoreLevel = oldlvl

#TODO!!!
def scale_by_width(g):
    for i in xrange(0,g.GetN()):
        g.GetY()[i] *= 1
    return g

def tg_add(g1,g2):
    g = copy.deepcopy( g1 )                                                                                                                

    for i in xrange(0,g.GetN()):
        g.SetPoint(i, g.GetX()[i], g1.GetY()[i]+g2.GetY()[i])
        g.SetPointError(i, 0, 0, g1.GetErrorYlow(i)*g1.GetErrorYlow(i)+g2.GetErrorYlow(i)*g2.GetErrorYlow(i), g1.GetErrorYhigh(i)*g1.GetErrorYhigh(i)+g2.GetErrorYhigh(i)*g2.GetErrorYhigh(i))
    return g

    #virtual voidSetPointError(Int_t i, Double_t exl, Double_t exh, Double_t eyl, Double_t eyh)

def isTGraph(g):
    if 'TGraph' in g.ClassName():
        return True
    else:
        return False

def isTH(g):
    if 'TH' in g.ClassName():
        return True
    else:
        return False

def same_binning(h1, h2):
    if h1.GetNbinsX() != h2.GetNbinsX(): return 0

    for i in xrange(1,h1.GetNbinsX()+2):
        if h1.GetBinLowEdge(i)!=h2.GetBinLowEdge(i): return 0

    return 1

def save_binning(h1, h2):
    nbins1=h1.GetNbinsX()
    nbins2=h2.GetNbinsX()

#    h2_rebin=R.TH1F( h2.GetName()+'_r', h2.GetTitle()+'_r', nbins1, binning )

#    print 'REB',get_binning(h2),nbins2
    h2_rebin=h2.Rebin(nbins1,"h2_rebin",binning);

#    for i1 in xrange(1,nbins1+1):
#        val=0
#        err2=0
#        bl=h1.GetBinLowEdge(i)
#        bh=h1.GetBinLowEdge(i+1)
#        for i2 in xrange(1,nbins2+1):
            

#    return None
#    for i in xrange(1,h1.GetNbinsX()+2):
#        if h1.GetBinLowEdge(i)!=h2.GetBinLowEdge(i): return 0

    return h2_rebin

def get_binning(h):
    nbins=h.GetNbinsX()
    xbins=[]

    for i in xrange(1,nbins+2):
        xbins+=[h.GetBinLowEdge(i)]

    a_xbins=array('d',xbins)

    return a_xbins


def graph_to_histo(g,asym=False):
  nbins=g.GetN()
  xbins=[]
  for i in xrange(0,nbins):
      xbins.append( g.GetX()[i]-g.GetErrorXlow(i) )
  xbins.append( g.GetX()[nbins-1]+g.GetErrorXlow(nbins-1) )


  a_xbins=array('d',xbins)

#  h=R.TH1F('h_'+g.GetName(),'h_'+g.GetTitle(), nbins, a_xbins)
  h=R.TH1F(g.GetName(),g.GetTitle(), nbins, a_xbins)
  for i in xrange(1,nbins+2):
      if asym:
          h.SetBinContent(i,g.GetY()[i-1]+ ( g.GetErrorYhigh(i-1)-g.GetErrorYlow(i-1) )/2 )
      else:
          h.SetBinContent(i,g.GetY()[i-1])
      h.SetBinError(i, ( g.GetErrorYlow(i-1)+g.GetErrorYhigh(i-1) )/2 )

  return h

def is_close(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

# def CreateTransparentColor(color, alpha):
#     print 'A',R.gROOT.GetListOfColors().GetLast()

#     adapt = R.gROOT.GetColor(color)
#     new_idx = R.gROOT.GetListOfColors().GetLast() + 1
#     trans = R.TColor(
#         new_idx, adapt.GetRed(), adapt.GetGreen(), adapt.GetBlue(), '', alpha)
#     COL_STORE.append(trans)
#     trans.SetName('userColor%i' % new_idx)

#     print 'B',R.gROOT.GetListOfColors().GetLast()

#     return new_idx

if __name__ == '__main__':
    main(sys.argv[1:])
