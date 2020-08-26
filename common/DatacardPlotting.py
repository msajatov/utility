import root_pandas as rp
import ROOT as R
import root_numpy as rn
import copy
import os
from math import sqrt
from array import array
R.gROOT.SetBatch(True)
R.gStyle.SetOptStat(0)
R.TGaxis.SetExponentOffset(-0.05, 0.01, "y")

class PlotSettings:
    def __init__(self, canvasType, signal, descriptions, era):
        self.canvasType = canvasType
        self.signal = signal
        self.descriptions = descriptions
        self.era = era

        self.textsize = 24
        self.cms1TextSize = self.textsize
        self.cms2TextSize = self.textsize * 0.875
        self.channelTextSize = self.textsize
        self.rightTopTextSize = self.textsize * 0.875

        self.axisTitleSize = 30

        # self.tickLabelSize = 24/(R.gPad.GetWh()*R.gPad.GetAbsHNDC())
        # self.axisLabelSize = 28/(R.gPad.GetWh()*R.gPad.GetAbsHNDC())

        if self.canvasType == "semi":
            self.semiInfoTextSize = self.textsize
            self.semiInfo_x = 0.3
            self.semiInfo_y = 0.1

        self.ratioTitle_x = 0.05
        self.ratioTitle_y = 0.2

        self.cms1_x = 0.17
        self.cms1_y = 0.93
        self.cms2_x = 0.245
        self.cms2_y = 0.93
        self.righttop_x = 0.4
        self.righttop_y = 0.93
        self.channel_x = 0.56
        self.channel_y = 0.93
    
        self.legendTextSize = self.textsize

        if self.canvasType == "semi":
            self.up_yLabelOffset = 0.015
            self.down_yLabelOffset = 0.007
            self.ratio_yLabelOffset = 0.015

            self.up_yTitleSize = 0.07*75/55
            self.down_yTitleSize = 0.07*75/55
            self.ratio_yTitleSize = 0.07*75/25
            self.ratioTitleTextSize = 0.07*75/25

            self.up_yTitleOffset = 2.2
            self.down_yTitleOffset = 2.1
            self.ratio_yTitleOffset = 2.1

        elif self.canvasType == "linear":
            self.up_yLabelOffset = 0.015
            self.ratio_yLabelOffset = 0.015

            self.up_yTitleSize = 0.07
            self.ratio_yTitleSize = 0.07*75/25
            self.ratioTitleTextSize = 0.07*75/25

            self.up_yTitleOffset = 2.2
            self.ratio_yTitleOffset = 2.1

        elif self.canvasType == "log":
            self.up_yLabelOffset = 0.015
            self.ratio_yLabelOffset = 0.015

            self.up_yTitleSize = 0.07
            self.ratio_yTitleSize = 0.07*75/25
            self.ratioTitleTextSize = 0.07*75/25

            self.up_yTitleOffset = 1.7
            self.ratio_yTitleOffset = 1.65

        self.ratio_xLabelOffset = 0.03

        self.ratio_xTitleSize = 0.2
        
        self.ratio_xTitleOffset = 5

        self.width=600 
        self.height=600

        self.maxVal = 0

    def setDimensions(self, width, height, leftMargin, topMargin, rightMargin, bottomMargin):

        self.cms1_x = leftMargin
        self.cms1_y = 1 - topMargin + 0.013 * 600 / height

        self.cms2_x = leftMargin + 0.11 * 600 / width
        self.cms2_y = self.cms1_y        

        self.channel_x = 1 - rightMargin - 0.42 * 600 / width
        self.channel_y = 1 - topMargin + 0.015 * 600 / height

        self.righttop_x = 1 - rightMargin - 0.34 * 600 / width
        self.righttop_y = 1 - topMargin + 0.015 * 600 / height

        # leftCornerPos = [leftMargin, 1 - topMargin + 0.01 * 600 / height]
        # rightCornerPos = [1 - rightMargin - 0.35 * 600 / width, 1 - topMargin + 0.012 * 600 / height]
        # midTopPos = [1 - rightMargin - 0.43 * 600 / width, 1 - topMargin + 0.012 * 600 / height]

def main():


    file = R.TFile("/afs/hephy.at/work/m/mspanring/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/htt_mt.inputs-sm-13TeV-eta_1.root")

    histos = {}
    for h in ["W","VVT","VVJ","TTT","TTJ","ZTT","ZL","ZJ","QCD","data_obs"]:
    # for h in ["VVT","TTT","ZTT","ZL","jetFakes_W","jetFakes_TT","jetFakes_QCD","data_obs"]:
    # for h in ["VVT","TTT","ZTT","ZL","jetFakes","data_obs"]:
        if h == "data_obs":
            histos["data"] = copy.deepcopy( file.Get("mt_inclusive/"+h) )
        else:
            histos[h] = copy.deepcopy( file.Get("mt_inclusive/"+h) ) 

    # histos = { "DY":R.TH1D("a","a",100,0,10),
    #            "QCD":R.TH1D("b","b",100,0,10),
    #            "data":R.TH1D("data","data",100,0,10), }




    # for i in xrange(1,100):
    #     histos["DY"].SetBinContent(i,i*0.1)
    #     histos["QCD"].SetBinContent(i,i*10)
    #     histos["data"].SetBinContent(i,i*0.1 + i*10)


    plot(histos,canvas = "linear")

def plot( histos, signal=[], canvas = "semi", outfile = "", descriptions = {}, era="", overlay=[] ):

    withSignal = (len(signal) > 0)
    settings = PlotSettings(canvas, withSignal, descriptions, era)
    content = generateContent(histos, signal, canvas, outfile, descriptions, era, overlay)

    if settings.canvasType == "semi":
        cv= createRatioSemiLogCanvas("cv", settings)

    if settings.canvasType == "linear":
        cv= createRatioCanvas("cv", settings)

    if settings.canvasType == "log":
        cv= createRatioCanvas("cv", settings)

    leg = prepareLegend(content, settings)

    dummies = prepareDummies(content, settings)

    objects = prepareObjects(settings)

    cv = draw(cv, content, dummies, objects, leg, settings)

    saveToFile(cv, outfile, canvas)

def generateContent(histos, signal=[], canvas = "semi", outfile = "", descriptions = {}, era="", overlay=[]):
    histos = copy.deepcopy(histos)

    if outfile and "/" in outfile:
        outdir = "/".join(outfile.split("/")[:-1])
        if not os.path.exists(outdir):
            os.mkdir(outdir)
    data = histos.pop("data",None)
    signal_hists = []

    for i,s in enumerate(signal):
        tmp = histos.pop(s, None)
        if tmp:
            applySignalHistStyle(tmp, s,3)
            signal_hists.append( tmp )
            
    yields = [ ( h.Integral(), name ) for name,h in histos.items() ]
    yields.sort()
    what = [ y[1] for y in yields ]

    cumul = copy.deepcopy(  histos[ what[0] ] )
    # cumul.SetFillColorAlpha(33,0.6)
    cumul.SetFillColorAlpha(15,0.6)
    cumul.SetLineWidth(0)
    cumul.SetLineColorAlpha(15,0.6)
    cumul.SetMarkerColorAlpha(15,0.0)

    applyHistStyle( histos[ what[0] ] , what[0] )

    stack = R.THStack("stack", "")
    stack.Add( copy.deepcopy( histos[ what[0] ] ) )
    
    for h in what[1:]:
        applyHistStyle( histos[h] , h )
        stack.Add( copy.deepcopy( histos[h] ) )
        cumul.Add( histos[h] )

    if not data:
        data = copy.deepcopy( cumul )

    ratio = copy.deepcopy( data )
    tmp = copy.deepcopy( cumul )
    for i in xrange( tmp.GetNbinsX() + 1 ):
        tmp.SetBinError(i,0.0)    
    ratio.Divide( tmp )

    ratio_error = copy.deepcopy( cumul )
    for i in xrange( ratio_error.GetNbinsX() + 1 ):
        ratio_error.SetBinError(i,0.0)
    ratio_error.Divide(cumul)
    # ratio_error.SetFillColorAlpha(33,0.7)
    ratio_error.SetFillColorAlpha(15,0.6)


    if signal:
        signal_ratio = copy.deepcopy( cumul )
        for s in signal_hists:
            signal_ratio.Add( copy.deepcopy( s ) )
        signal_ratio.Divide(cumul)
        applySignalHistStyle(signal_ratio, "sig", 2 )


    applySignalHistStyle(data, "data")
    applySignalHistStyle(ratio, "data")

    content = {}
    content["data"] = data
    content["stack"] = stack
    content["cumul"] = cumul
    content["ratio"] = ratio
    content["ratio_error"] = ratio_error

    content["what"] = what
    content["signal_hists"] = signal_hists

    content["histos"] = histos

    if signal:
        content["signal_ratio"] = signal_ratio

    return content

def prepareObjects(settings): 

    cms1 = R.TLatex( settings.cms1_x, settings.cms1_y, "CMS" )
    cms2 = R.TLatex( settings.cms2_x, settings.cms2_y, settings.descriptions.get( "plottype", "ProjectWork" ) )

    chtex = {"et": r"#font[42]{#scale[0.95]{e}}#tau_{#lower[-0.1]{h}}", "mt": r"#mu"r"#tau_{#lower[-0.3]{h}}", "tt": r"#tau_{#lower[-0.1]{h}}#tau_{#lower[-0.1]{h}}", "em": r"e#mu"}
    ch = settings.descriptions.get( "channel", "  " )
    ch = chtex.get(ch,ch)
    channel = R.TLatex( settings.channel_x, settings.channel_y, ch )

    lumi = settings.descriptions.get( "lumi", "xx.y" )
    som = settings.descriptions.get( "CoM", "13" )
    era = settings.descriptions.get("era", "2017")
    l = lumi + r" fb^{-1}"
    r = " ({1}, {0} TeV)".format(som, settings.era)
    righttop = R.TLatex( settings.righttop_x, settings.righttop_y, l+r)

    cms1.SetNDC()
    cms2.SetNDC()
    righttop.SetNDC()
    channel.SetNDC()

    cms1.SetTextSize(settings.cms1TextSize)    
    cms1.SetTextFont(63)       
    cms2.SetTextFont(43)
    cms2.SetTextSize(settings.cms2TextSize)
    righttop.SetTextSize(settings.rightTopTextSize)
    righttop.SetTextFont(63)
    channel.SetTextSize(settings.channelTextSize)
    channel.SetTextFont(43)

    if settings.canvasType == "semi":
        semi_info = R.TLatex( settings.semiInfo_x, settings.semiInfo_y, "log-scale")
        semi_info.SetTextFont(43)
        semi_info.SetTextAngle(90)
        semi_info.SetNDC()
        semi_info.SetTextSize(settings.semiInfoTextSize)
        semi_info.SetTextColor(  R.TColor.GetColor(125,125,125) )

    ratio_title = R.TLatex( settings.ratioTitle_x, settings.ratioTitle_y, "Obs./Exp.")
    ratio_title.SetTextFont(42)
    ratio_title.SetTextAngle(90)
    ratio_title.SetNDC()
    ratio_title.SetTextSize(settings.ratioTitleTextSize)

    objects = {}
    objects["cms1"] = cms1
    objects["cms2"] = cms2
    objects["righttop"] = righttop
    objects["channel"] = channel

    objects["ratio_title"] = ratio_title

    if settings.canvasType == "semi":
        objects["semi_info"] = semi_info

    return objects

def adjustSettings(settings):
    pass

def prepareLegend(content, settings): 
    canvas = settings.canvasType

    if canvas == "semi":                      
        leg = R.TLegend(0.65, 1 - 0.5*75/55, 0.96, 1 - 0.10*75/55)
        # leg.SetTextSize(0.04*75/55)
    if canvas == "linear" or canvas == "log":
        leg = R.TLegend(0.65, 0.5, 0.96, 0.90)
        # leg.SetTextSize(0.04)
        
    # leg.SetBorderSize(0)

    # dummy_err = TH1F("Uncertainty")
    # dummy_err.SetFillColor( getColor( name ) )
    # dummy_err.SetLineColor( R.kBlack )
    
    leg.AddEntry( content["data"], "Obs. Data")

    for n in reversed(content["what"]):
        leg.AddEntry( content["histos"][n], getFancyName(n), "f" )
    for s in content["signal_hists"]:
        leg.AddEntry( s, getFancyName( s.GetName() ), "f" )

    leg.AddEntry(content["cumul"], "Uncertainty", "f")

    leg.SetTextSize(settings.legendTextSize)
    leg.SetTextFont(43)     
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineWidth(0)
    leg.SetFillStyle(0)

    return leg

def prepareDummies(content, settings):

    dummies = {}

    data = content["data"]
    stack = content["stack"]
    cumul = content["cumul"]
    ratio = content["ratio"]
    ratio_error = content["ratio_error"] 

    settings.maxVal = max( stack.GetMaximum(), data.GetMaximum() ) * 1.2
    dummy_up    = copy.deepcopy( data )
    dummy_up.Reset()
    dummy_up.SetTitle("")

    dummy_up.GetYaxis().SetTitleSize(settings.axisTitleSize)    
    dummy_up.GetYaxis().SetTitleOffset(settings.up_yTitleOffset)
    dummy_up.GetYaxis().SetTitleFont(43)
    
    dummy_up.GetYaxis().SetLabelSize(25.0)
    dummy_up.GetYaxis().SetTitle( r"Event Count" )

    dummy_up.GetYaxis().SetLabelOffset(settings.up_yLabelOffset)

    dummies["up"] = dummy_up

    if settings.canvasType == "semi":
        dummy_down  = copy.deepcopy( data )
        dummy_down.Reset()
        dummy_down.SetTitle("")
        dummy_down.GetYaxis().SetRangeUser( 0.1 , settings.maxVal/ 40 )
        dummy_down.GetYaxis().SetLabelSize(25.0)
        dummy_down.GetXaxis().SetLabelSize(0)
        dummy_down.GetXaxis().SetTitle("")
        dummy_down.GetYaxis().SetTitleFont(43)
        dummy_down.GetYaxis().SetTitleSize(settings.axisTitleSize)   

        dummy_down.GetYaxis().SetLabelOffset(settings.down_yLabelOffset)

        dummies["down"] = dummy_down    

    dummy_ratio = copy.deepcopy( ratio )
    dummy_ratio.Reset()
    dummy_ratio.SetTitle("")
    dummy_ratio.GetYaxis().SetRangeUser( 0.7 , 1.3 )
    dummy_ratio.GetYaxis().SetNdivisions(4)
    dummy_ratio.GetYaxis().SetLabelSize(25.0)
    dummy_ratio.GetXaxis().SetTitleFont(43)
    dummy_ratio.GetXaxis().SetTitleSize(settings.axisTitleSize)
    dummy_ratio.GetXaxis().SetTitleOffset(settings.ratio_xTitleOffset)
    dummy_ratio.GetXaxis().SetLabelSize(25.0)
    dummy_ratio.GetXaxis().SetTitle( settings.descriptions.get( "xaxis", "some quantity" ) )

    dummy_ratio.GetYaxis().SetTitle( r"Obs./Exp." )
    dummy_ratio.GetYaxis().SetTitleFont(43)
    dummy_ratio.GetYaxis().SetTitleSize(settings.axisTitleSize) 
    dummy_ratio.GetYaxis().SetTitleOffset(settings.ratio_yTitleOffset)

    dummy_ratio.GetXaxis().SetLabelOffset(settings.ratio_xLabelOffset)
    dummy_ratio.GetYaxis().SetLabelOffset(settings.ratio_yLabelOffset)

    dummies["ratio"] = dummy_ratio    
    
    # print dummy_ratio.GetXaxis().GetLabelSize()
    # print dummy_ratio.GetXaxis().GetLabelOffset()
    # print dummy_ratio.GetYaxis().GetLabelOffset()
    # print dummy_up.GetYaxis().GetLabelOffset()
    # print dummy_down.GetYaxis().GetLabelOffset()       
    
    # print dummy_ratio.GetXaxis().GetLabelSize()
    # print dummy_ratio.GetXaxis().GetLabelOffset()
    # print dummy_ratio.GetYaxis().GetLabelOffset()
    # print dummy_up.GetYaxis().GetLabelOffset()
    # print dummy_down.GetYaxis().GetLabelOffset()

    return dummies

def draw(cv, content, dummies, objects, leg, settings):

    print "Entering draw..."
    canvas = settings.canvasType

    dummy_up = dummies["up"]
    dummy_ratio = dummies["ratio"]

    if canvas == "semi":
        dummy_down = dummies["down"]    

    data = content["data"]
    stack = content["stack"]
    cumul = content["cumul"]
    ratio = content["ratio"]
    ratio_error = content["ratio_error"] 

    if settings.signal:
        signal_ratio = content["signal_ratio"]

    if canvas == "semi":
        dummy_up.GetYaxis().SetRangeUser( settings.maxVal/ 40 , settings.maxVal )
        # cv= createRatioSemiLogCanvas("cv", settings)

    if canvas == "linear":
        dummy_up.GetYaxis().SetRangeUser( 0 , settings.maxVal )
        dummy_up.GetXaxis().SetLabelSize(0)
        # cv= createRatioCanvas("cv", settings)

    if canvas == "log":
        dummy_up.GetYaxis().SetRangeUser( 0.1 , settings.maxVal * 2 )
        dummy_up.GetXaxis().SetLabelSize(0)
        # cv= createRatioCanvas("cv", settings)

    ## draw upper pad
    cv.cd(1)

    if canvas == "log": 
        R.gPad.SetLogy()  

    dummy_up.Draw()
    stack.Draw("same hist")
    cumul.Draw("same e2")

    if canvas == "semi":
        data.Draw("same e")
    else:
        # data.Draw("same e1")
        data.Draw("same e")

    leg.Draw()
    R.gPad.RedrawAxis()

    ## draw ratio pad
    if canvas == "semi":
        cv.cd(3)
    else:
        cv.cd(2)

    dummy_ratio.Draw()
    ratio_error.Draw("same e2")

    if canvas == "semi":
        ratio.Draw("same e")
    else:
        # ratio.Draw("same e1")
        ratio.Draw("same e")

    # objects["ratio_title"].Draw()

    if settings.signal:
        signal_ratio.Draw("same hist")

    R.gPad.RedrawAxis()
    
    ## if semi, draw lower pad
    if canvas == "semi":
        cv.cd(2)
        dummy_down.Draw()
        stack.Draw("same hist")
        cumul.Draw("same e2")
        data.Draw("same e1")
        # for s in signal_hists:
        #     s.Draw("same hist")

        R.gPad.RedrawAxis()

    ## draw remaining objects
    cv.cd(1)
    objects["cms1"].Draw()
    objects["cms2"].Draw()
    objects["channel"].Draw()
    objects["righttop"].Draw()

    # if canvas == "semi":
    #     objects["semi_info"].Draw()

    if canvas == "semi":
        cv.cd(2)
    else:
        cv.cd(1)

    R.gPad.Update()
    R.gPad.RedrawAxis()
    line = R.TLine()

    if canvas == "semi":  
        line.DrawLine(R.gPad.GetUxmax(), R.gPad.GetUymin(), R.gPad.GetUxmax(), settings.maxVal/ 40)
    else:
        line.DrawLine(R.gPad.GetUxmax(), R.gPad.GetUymin(), R.gPad.GetUxmax(), settings.maxVal)  

    return cv

def saveToFile(cv, outfile, canvas):
    if not outfile:
        outfile = "{0}_canvas.png".format(canvas)

    cvname = os.path.basename(outfile)
    cvname = cvname.replace(".png", "")
    cvname = cvname.replace(".root", "")

    cv.SetName(cvname)    
    
    outfile = outfile.replace(".png", "_" + canvas + ".png")
    filename = outfile
    print filename
    cv.SaveAs(filename)
    # filename = outfile.replace(".png", ".root")
    # print filename
    # cv.SaveAs(filename)
    filename = outfile.replace(".png", ".pdf")
    print filename
    cv.SaveAs(filename)
    filename = outfile.replace(".png", ".svg")
    print filename
    cv.SaveAs(filename)

def createRatioSemiLogCanvas(name, settings, width=600, height=700):

    cv = R.TCanvas(name, name, 10, 10, width, height)

    # this is the tricky part...
    # Divide with correct margins
    cv.Divide(1, 3, 0.0, 0.0)

    # Set Pad sizes
    cv.GetPad(1).SetPad(0.0, 0.45, 1., 1.0)
    cv.GetPad(2).SetPad(0.0, 0.25, 1., 0.465)
    cv.GetPad(3).SetPad(0.0, 0.00, 1., 0.25)

    cv.GetPad(1).SetFillStyle(4000)
    cv.GetPad(2).SetFillStyle(4000)
    cv.GetPad(3).SetFillStyle(4000)

    lmargin = 0.19
    rmargin = 0.05
    tmargin = 0.08
    bmargin = 0.5

    # Set pad margins 1
    cv.cd(1)
    R.gPad.SetTopMargin(tmargin)
    R.gPad.SetBottomMargin(0)
    R.gPad.SetLeftMargin(lmargin)
    R.gPad.SetRightMargin(rmargin)

    cv.cd(2)
    R.gPad.SetTopMargin(0.05)
    R.gPad.SetLeftMargin(lmargin)
    R.gPad.SetBottomMargin(0.08)
    R.gPad.SetRightMargin(rmargin)
    R.gPad.SetLogy()

    # Set pad margins 2
    cv.cd(3)
    R.gPad.SetTopMargin(0.03)
    R.gPad.SetBottomMargin(bmargin)
    R.gPad.SetLeftMargin(lmargin)
    R.gPad.SetRightMargin(rmargin)
    R.gPad.SetGridy()

    settings.setDimensions(width, height, lmargin, tmargin, rmargin, bmargin)

    cv.cd(1)
    return cv

def createRatioCanvas(name, settings, width=600, height=700):

    cv = R.TCanvas(name, name, 10, 10, width, height)

    # this is the tricky part...
    # Divide with correct margins
    cv.Divide(1, 2, 0.0, 0.0)

    # Set Pad sizes
    cv.GetPad(1).SetPad(0.0, 0.25, 1., 1.0)
    cv.GetPad(2).SetPad(0.0, 0.00, 1., 0.25)

    cv.GetPad(1).SetFillStyle(4000)
    cv.GetPad(2).SetFillStyle(4000)

    if settings.canvasType == "linear":
        # lmargin = 0.18
        lmargin = 0.19
        # rmargin = 0.03
        rmargin = 0.04
    else:
        lmargin = 0.15
        rmargin = 0.02

    tmargin = 0.06 * 4 / 3
    # tmargin = 0.08

    R.gStyle.SetGridStyle(1)
    R.gStyle.SetGridColor(15)
    # R.gStyle.SetGridWidth(3)

    # Set pad margins 1
    cv.cd(1)
    R.gPad.SetTopMargin(tmargin)
    # R.gPad.SetBottomMargin(0.015)
    R.gPad.SetBottomMargin(0.025)
    R.gPad.SetLeftMargin(lmargin)
    R.gPad.SetRightMargin(rmargin)

    bmargin = 0.5

    cv.cd(2)
    # R.gPad.SetTopMargin(0.03)
    R.gPad.SetTopMargin(0.00)
    R.gPad.SetBottomMargin(bmargin)
    R.gPad.SetLeftMargin(lmargin)
    R.gPad.SetRightMargin(rmargin)
    R.gPad.SetGridy()

    settings.setDimensions(width, height, lmargin, tmargin, rmargin, bmargin)

    cv.cd(1)
    return cv

def applyHistStyle(hist, name):

    hist.GetXaxis().SetLabelFont(43)
    hist.GetXaxis().SetLabelSize(14)
    hist.GetYaxis().SetLabelFont(43)
    hist.GetYaxis().SetLabelSize(14)
    hist.SetFillColor( getColor( name ) )
    hist.SetLineColor( R.kBlack )

def applySignalHistStyle(hist, name, width = 1):

    hist.GetXaxis().SetLabelFont(43)
    hist.GetXaxis().SetLabelSize(14)
    hist.GetYaxis().SetLabelFont(43)
    hist.GetYaxis().SetLabelSize(14)
    hist.SetFillColor( 0 )
    hist.SetLineWidth( width )
    hist.SetLineColor( getColor( name ) )
    hist.SetMarkerStyle(9)
    hist.SetMarkerSize(0.8)


def getFancyName(name):
    if name == "ZL":                return r"Z (l #rightarrow #tau)"
    if name == "ZJ":                return r"Z (Jet #rightarrow #tau)"
    if name == "ZTT":               return r"Z #rightarrow #tau#tau"
    if name == "EMB":         return r"Genuine #tau#tau"
    if name == "TTT":               return r"t#bar{t} (#tau #rightarrow #tau)"
    if name == "TTJ":               return r"t#bar{t} (Jet #rightarrow #tau)"
    if name == "TTL":               return r"t#bar{t} (l #rightarrow #tau)"    
    if name == "VVT":               return r"VV (#tau#rightarrow #tau)"
    if name == "VVJ":               return r"VV (Jet #rightarrow #tau)"
    if name == "VVL":               return r"VV (l #rightarrow #tau)"    
    if name == "W":                 return r"W + jet"
    if name == "QCD":               return r"MultiJet"
    if name == "jetFakes":          return r"Jet #rightarrow #tau_{h}"
    if name == "jetFakes_W":        return r"W + jet ( F_{F} )"
    if name == "jetFakes_TT":       return r"t#bar{t} ( F_{F} )"
    if name == "jetFakes_QCD":      return r"MultiJet ( F_{F} )"    
    if name == "EWKZ":              return r"EWKZ"
    if name in ["qqH","qqH125"]:    return "VBF"
    if name in ["ggH","ggH125"]:    return "ggF"

    return name



def getColor(name):

    if name in ["TT","TTT","TTJ","jetFakes_TT","TTL", "tt"]:    return R.TColor.GetColor(155,152,204)
    if name in ["sig"]:                             return R.kRed
    if name in ["bkg"]:                             return R.kBlue
    if name in ["qqH","qqH125"]:                    return R.TColor.GetColor(0,100,0)
    if name in ["ggH","ggH125"]:                    return R.TColor.GetColor(0,0,100)
    if name in ["W","jetFakes_W", "w"]:                  return R.TColor.GetColor(222,90,106)
    if name in ["VV","VVJ","VVT","VVL"]:            return R.TColor.GetColor(175,35,80)
    if name in ["ZL","ZJ","ZLJ"]:                   return R.TColor.GetColor(100,192,232)
    if name in ["EWKZ"]:                            return R.TColor.GetColor(8,247,183)
    if name in ["QCD","WSS","jetFakes_QCD", "qcd"]:        return R.TColor.GetColor(250,202,255)
    if name in ["ZTT","DY","real","EMB", "dy"]:           return R.TColor.GetColor(248,206,104)
    if name in ["jetFakes"]:                        return R.TColor.GetColor(192,232,100)
    if name in ["data"]:                            return R.TColor.GetColor(0,0,0)
    else: return R.kYellow

if __name__ == '__main__':
    main()
