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


def simple_plot(histograms, signal=[], canvas="linear", outfile="", descriptions={}, optimizeTicks=True, legend="outer"):

    histos = copy.deepcopy(histograms)

    cumul = copy.deepcopy(histos[0][1])
    cumul.SetFillColorAlpha(33, 0.6)
    applyHistStyle(histos[0][1], histos[0][0])
    histos[0][1].SetName(histos[0][0])

    stack = R.THStack("stack", "")
    stack.Add(copy.deepcopy(histos[0][1]))

    for h in histos[1:]:
        "Calling applyHistStyle:"
        applyHistStyle(h[1], h[0])
        h[1].SetName(h[0])
        stack.Add(copy.deepcopy(h[1]))
        cumul.Add(h[1])
            
    topTextSize = 0.035
    cms1TextSize = topTextSize
    cms2TextSize = topTextSize * 0.875
    channelTextSize = topTextSize
    rightTopTextSize = topTextSize * 0.875

    tickLabelSize = 0.04
    axisLabelSize = 0.05
    legendTextSize = 0.04
    
    width=600 
    height=600   
        
    topMargin=0.08
    bottomMargin=0.2
    leftMargin=0.22
    rightMargin=0.05       

    legWidth = 150.0
    relLegWidth = legWidth / width
        
    leg = R.TLegend(1 - relLegWidth - 0.05, 0.65, 1 - 0.08, 1 - topMargin - 0.07)  

    if legend == "outer":
        originalWidth = width
        legWidth = 100
        width = int(originalWidth + legWidth)
        height = 600   
            
        topMargin=0.08
        bottomMargin=0.2
        leftMargin=0.22 * originalWidth / width
        rightMargin = 1 - width / originalWidth
            
        leg = R.TLegend(1 - rightMargin + 0.02, 0.70, 1 - 0.02, 1 - topMargin)    

    for h in reversed(histos):
        leg.AddEntry(h[1], " " + getFancyName(h[0]), "f")

    leg.SetTextSize(legendTextSize)
    leg.SetBorderSize(0)
    leg.SetFillColor(10)
    leg.SetLineWidth(0)
    leg.SetFillStyle(0)

    maxVal = stack.GetMaximum()
    dummy_up = copy.deepcopy(cumul)
    dummy_up.Reset()
    dummy_up.SetTitle(descriptions.get("title", ""))
    dummy_up.GetYaxis().SetRangeUser(0.5, 1.5)
    dummy_up.GetYaxis().SetNdivisions(10, 4, 0, optimizeTicks)
    dummy_up.GetYaxis().SetTickSize(0.02)
    dummy_up.GetYaxis().SetTitle(descriptions.get("yaxis", "some quantity"))
    dummy_up.GetYaxis().SetTitleSize(axisLabelSize)
    dummy_up.GetYaxis().SetLabelSize(tickLabelSize)
    
    dummy_up.GetXaxis().SetTickSize(0.02)
    dummy_up.GetXaxis().SetTitleSize(0.03)
    dummy_up.GetXaxis().SetTitle(descriptions.get("xaxis", "some quantity"))
    dummy_up.GetXaxis().SetTitleOffset(1.15)
    dummy_up.GetXaxis().SetTitleSize(axisLabelSize)
    dummy_up.GetXaxis().SetLabelSize(tickLabelSize)

    dummy_down = copy.deepcopy(cumul)
    dummy_down.Reset()
    dummy_down.SetTitle("")
    dummy_down.GetYaxis().SetRangeUser(0.1, maxVal / 40)
    dummy_down.GetXaxis().SetLabelSize(0)
    dummy_down.GetXaxis().SetTitle("")

    leftCornerPos = [leftMargin, 1 - topMargin + 0.01 * 600 / height]
    rightCornerPos = [1 - rightMargin - 0.24 * 700 / width, 1 - topMargin + 0.012 * 600 / height]
    midTopPos = [1 - rightMargin - 0.29 * 700 / width, 1 - topMargin + 0.012 * 600 / height]

    cms1 = R.TLatex(leftCornerPos[0], leftCornerPos[1], "CMS")
    cms2 = R.TLatex(leftCornerPos[0] + 0.09, leftCornerPos[1], descriptions.get("plottype", "Project Work"))
    
    
    chtex = {"et": r"#font[42]{#scale[0.95]{e}}#tau", "mt": r"#mu#tau", "tt": r"#tau#tau", "em": r"e#mu"}
    ch = descriptions.get("channel", "  ")
    ch = chtex.get(ch, ch)
    channel = R.TLatex(midTopPos[0], midTopPos[1], ch )

    lumi = descriptions.get("lumi", "xx.y")
    som = descriptions.get("CoM", "13")
    era = descriptions.get("era", "2017")
    l = lumi + r" fb^{-1}"
    r = " ({0}, {1} TeV)".format(era, som)
    righttop = R.TLatex(rightCornerPos[0], rightCornerPos[1], l + r)

    cms1.SetNDC()
    cms2.SetNDC()
    righttop.SetNDC()
    channel.SetNDC()

    dummy_up.GetYaxis().SetRangeUser(0, maxVal)

    cv = createSimpleCanvas("cv", width, height, topMargin, bottomMargin, leftMargin, rightMargin)

    cv.cd(1)
    
    cms1.SetTextSize(cms1TextSize)           
    cms2.SetTextFont(52)
    cms2.SetTextSize(cms2TextSize)
    righttop.SetTextSize(rightTopTextSize)
    righttop.SetTextFont(42)
    channel.SetTextSize(channelTextSize)

    dummy_up.Draw()
    stack.Draw("same hist ")
    leg.Draw()
    R.gPad.RedrawAxis()

    if not outfile:
        outfile = "{0}_canvas.png".format(canvas)

    cv.cd(1)
    cms1.Draw()
    cms2.Draw()
    channel.Draw()
    righttop.Draw()

    cvname = os.path.basename(outfile)
    cvname = cvname.replace(".png", "")
    cvname = cvname.replace(".root", "")

    cv.SetName(cvname)

    filename = outfile
    print filename
    cv.SaveAs(filename)
    filename = outfile.replace(".png", ".root")
    print filename
    cv.SaveAs(filename)
    filename = outfile.replace(".png", ".pdf")
    print filename
    cv.SaveAs(filename)


def plot( histograms, signal=[], canvas = "semi", outfile = "", descriptions = {} ):

    histos = copy.deepcopy(histograms)

    print "Entering plot..."

    data = histos.pop("data",None)
    signal_hists = []

    print "Length of histos:"
    print str(len(histos))

    for i,s in enumerate(signal):
        tmp = histos.pop(s, None)
        if tmp:
            applySignalHistStyle(tmp, s,3)
            signal_hists.append( tmp )
            
    yields = [ ( h.Integral(), name ) for name,h in histos.items() ]
    yields.sort()
    what = [ y[1] for y in yields ]

    cumul = copy.deepcopy(  histos[ what[0] ] )
    cumul.SetFillColorAlpha(33,0.6);
    applyHistStyle( histos[ what[0] ] , what[0] )

    stack = R.THStack("stack", "")
    stack.Add( copy.deepcopy( histos[ what[0] ] ) )
    
    for h in what[1:]:
        "Calling applyHistStyle:"
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
    ratio_error.SetFillColorAlpha(33,0.7)


    if signal:
        signal_ratio = copy.deepcopy( cumul )
        for s in signal_hists:
            signal_ratio.Add( copy.deepcopy( s ) )
        signal_ratio.Divide(cumul)
        applySignalHistStyle(signal_ratio, "sig", 2 )


    applySignalHistStyle(data, "data")
    applyHistStyle(ratio, "")

    if canvas == "semi":                      
        leg = R.TLegend(0.82, 0.03, 0.98, 0.92)
        leg.SetTextSize(0.05)
    if canvas == "linear" or canvas == "log":
        leg = R.TLegend(0.82, 0.29, 0.98, 0.92)
        leg.SetTextSize(0.035)
    
    leg.AddEntry( data, "data obs." )

    for n in reversed(what):
        leg.AddEntry( histos[n], getFancyName(n) )
    for s in signal_hists:
        leg.AddEntry( s, getFancyName( s.GetName() ) )


    maxVal = max( stack.GetMaximum(), data.GetMaximum() ) * 1.2
    dummy_up    = copy.deepcopy( data )
    dummy_up.Reset()
    dummy_up.SetTitle("")

    dummy_down  = copy.deepcopy( data )
    dummy_down.Reset()
    dummy_down.SetTitle("")
    dummy_down.GetYaxis().SetRangeUser( 0.1 , maxVal/ 40 )
    dummy_down.GetXaxis().SetLabelSize(0)
    dummy_down.GetXaxis().SetTitle("")

    dummy_ratio = copy.deepcopy( ratio )
    dummy_ratio.Reset()
    dummy_ratio.SetTitle("")
    dummy_ratio.GetYaxis().SetRangeUser( 0.5 , 1.5 )
    dummy_ratio.GetYaxis().SetNdivisions(6)
    dummy_ratio.GetXaxis().SetTitleSize(0.12)
    dummy_ratio.GetXaxis().SetTitleOffset(1)
    dummy_ratio.GetXaxis().SetTitle( descriptions.get( "xaxis", "some quantity" ) )

    cms1 = R.TLatex( 0.08, 0.93, "CMS" )
    cms2 = R.TLatex( 0.135, 0.93, descriptions.get( "plottype", "ProjectWork" ) )

    chtex = {"et":r"e#tau","mt":r"#mu#tau","tt":r"#tau#tau","em":r"e#mu"}
    ch = descriptions.get( "channel", "  " )
    ch = chtex.get(ch,ch)
    channel = R.TLatex( 0.60, 0.932, ch )

    lumi = descriptions.get( "lumi", "xx.y" )
    som = descriptions.get( "CoM", "13" )
    l = lumi + r" fb^{-1}"
    r = " ({0} TeV)".format(som)
    righttop = R.TLatex( 0.655, 0.932, l+r)



    cms1.SetNDC();
    cms2.SetNDC();
    righttop.SetNDC();
    channel.SetNDC();

    if canvas == "semi":
        cms1.SetTextSize(0.055)            
        cms2.SetTextFont(12)
        cms2.SetTextSize(0.055)
        righttop.SetTextSize(0.05)
        channel.SetTextSize(0.06)

        semi_info = R.TLatex( 0.83, 0.2, "log-scale")
        semi_info.SetTextAngle(90)
        semi_info.SetNDC();
        semi_info.SetTextSize(0.15)
        semi_info.SetTextColor(  R.TColor.GetColor(125,125,125) )

    if canvas == "linear" or canvas == "log":
        cms1.SetTextSize(0.04);            
        cms2.SetTextFont(12)
        cms2.SetTextSize(0.04);
        righttop.SetTextSize(0.035);
        channel.SetTextSize(0.045)


    if canvas == "semi":
        dummy_up.GetYaxis().SetRangeUser( maxVal/ 40 , maxVal )

        cv= createRatioSemiLogCanvas("cv" )

        cv.cd(1)
        dummy_up.Draw()
        stack.Draw("same hist")
        cumul.Draw("same e2")
        data.Draw("same e1")
        leg.Draw()
        R.gPad.RedrawAxis()
        cv.cd(2)
        dummy_down.Draw()
        stack.Draw("same hist")
        cumul.Draw("same e2")
        data.Draw("same e1")
        for s in signal_hists:
            s.Draw("same hist")

        semi_info.Draw()

        R.gPad.RedrawAxis()
        cv.cd(3)
        dummy_ratio.Draw()
        ratio_error.Draw("same e2")
        ratio.Draw("same e1")
        if signal:
            signal_ratio.Draw("same hist")
        R.gPad.RedrawAxis()

    if canvas == "linear" or canvas == "log":

        if canvas == "linear": dummy_up.GetYaxis().SetRangeUser( 0 , maxVal )
        if canvas == "log": dummy_up.GetYaxis().SetRangeUser( 0.1 , maxVal )
        dummy_up.GetXaxis().SetLabelSize(0)

        cv= createRatioCanvas("cv" )

        cv.cd(1)
        if canvas == "log": R.gPad.SetLogy()

        dummy_up.Draw()
        stack.Draw("same hist ")
        cumul.Draw("same e2")
        data.Draw("same e1")
        leg.Draw()
        R.gPad.RedrawAxis()
        cv.cd(2)
        dummy_ratio.Draw()
        ratio_error.Draw("same e2")
        ratio.Draw("same e1")
        if signal:
            signal_ratio.Draw("same hist")
        R.gPad.RedrawAxis()
    
    if not outfile:
        outfile = "{0}_canvas.png".format(canvas)

    cv.cd(1)
    cms1.Draw()
    cms2.Draw()
    channel.Draw()
    righttop.Draw()

    cvname = os.path.basename(outfile)
    cvname = cvname.replace(".png", "")
    cvname = cvname.replace(".root", "")

    cv.SetName(cvname)

    cv.SaveAs(outfile.replace(".root", ".png"))
    cv.SaveAs(outfile.replace(".png", ".root"))
    


def createSimpleCanvas(name, width=700, height=600, topMargin=0.08, bottomMargin=0.12,
                       leftMargin=0.08, rightMargin=0.15):

    cv = R.TCanvas(name, name, 10, 10, width, height)
    cv.Divide(1, 1, 0.0, 0.0)

    # Set Pad sizes
    cv.GetPad(1).SetPad(0.0, 0.0, 1.0, 1.0)
    cv.GetPad(1).SetFillStyle(4000)

    # Set pad margins 1
    cv.cd(1)
    R.gPad.SetTopMargin(topMargin)
    R.gPad.SetBottomMargin(bottomMargin)
    R.gPad.SetLeftMargin(leftMargin)
    R.gPad.SetRightMargin(rightMargin)
    return cv



def createRatioSemiLogCanvas(name):

    cv = R.TCanvas(name, name, 10, 10, 800, 600)

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

    # Set pad margins 1
    cv.cd(1)
    R.gPad.SetTopMargin(0.08)
    R.gPad.SetBottomMargin(0)
    R.gPad.SetLeftMargin(0.08)
    R.gPad.SetRightMargin(0.2)

    cv.cd(2)
    R.gPad.SetTopMargin(0.05)
    R.gPad.SetLeftMargin(0.08)
    R.gPad.SetBottomMargin(0.05)
    R.gPad.SetRightMargin(0.2)
    R.gPad.SetLogy()

    # Set pad margins 2
    cv.cd(3)
    R.gPad.SetTopMargin(0.03)
    R.gPad.SetBottomMargin(0.3)
    R.gPad.SetLeftMargin(0.08)
    R.gPad.SetRightMargin(0.2)
    R.gPad.SetGridy()

    cv.cd(1)
    return cv

def createRatioCanvas(name):

    cv = R.TCanvas(name, name, 10, 10, 800, 600)

    # this is the tricky part...
    # Divide with correct margins
    cv.Divide(1, 2, 0.0, 0.0)

    # Set Pad sizes
    cv.GetPad(1).SetPad(0.0, 0.25, 1., 1.0)
    cv.GetPad(2).SetPad(0.0, 0.00, 1., 0.25)

    cv.GetPad(1).SetFillStyle(4000)
    cv.GetPad(2).SetFillStyle(4000)

    # Set pad margins 1
    cv.cd(1)
    R.gPad.SetTopMargin(0.08)
    R.gPad.SetBottomMargin(0.01)
    R.gPad.SetLeftMargin(0.08)
    R.gPad.SetRightMargin(0.2)

    cv.cd(2)
    R.gPad.SetTopMargin(0.03)
    R.gPad.SetBottomMargin(0.3)
    R.gPad.SetLeftMargin(0.08)
    R.gPad.SetRightMargin(0.2)
    R.gPad.SetGridy()

    cv.cd(1)
    return cv

def applyHistStyle(hist, name):
    # print "Applying hist style:"
    hist.GetXaxis().SetLabelFont(63)
    hist.GetXaxis().SetLabelSize(14)
    hist.GetYaxis().SetLabelFont(63)
    hist.GetYaxis().SetLabelSize(14)
    hist.SetFillColor( getColor( name ) )
    hist.SetLineColor( R.kBlack )
    #hist.SetLineColor(1)
    #hist.SetLineStyle(0)
    #hist.SetFillStyle(1001)

def applySignalHistStyle(hist, name, width = 1):
    # print "Applying signal hist style:"
    hist.GetXaxis().SetLabelFont(63)
    hist.GetXaxis().SetLabelSize(14)
    hist.GetYaxis().SetLabelFont(63)
    hist.GetYaxis().SetLabelSize(14)
    hist.SetFillColor( 0 )
    hist.SetLineWidth( width )
    hist.SetLineColor( getColor( name ) )


def getFancyName(name):
    if name == "ZL":                return r"Z (l#rightarrow#tau)"
    if name == "ZJ":                return r"Z (jet#rightarrow#tau)"
    if name == "ZTT":               return r"Z #rightarrow #tau#tau"
    if name == "TTT":               return r"t#bar{t} (#tau#rightarrow#tau)"
    if name == "TTJ":               return r"t#bar{t} (jet#rightarrow#tau)"
    if name == "VVT":               return r"VV (#tau#rightarrow#tau)"
    if name == "VVJ":               return r"VV (jet#rightarrow#tau)"
    if name == "W":                 return r"W + jet"
    if name == "QCD":               return r"MultiJet"
    if name == "jetFakes":          return r"jet #rightarrow #tau_{h}"
    if name == "jetFakes_W":        return r"W + jet ( F_{F} )"
    if name == "jetFakes_TT":       return r"t#bar{t} ( F_{F} )"
    if name == "jetFakes_QCD":      return r"MultiJet ( F_{F} )"    
    if name == "EWKZ":              return r"EWKZ"
    if name in ["qqH","qqH125"]:    return "VBF"
    if name in ["ggH","ggH125"]:    return "ggF"

    return name



def getColor(name):
    # print "Name in getColor is:"
    # print name
    if name in ["TT","TTT","TTJ","jetFakes_TT", "tt", "TTT_anti", "TTJ_anti", "TTL_anti"]:    return R.TColor.GetColor(155,152,204)
    if name in ["sig"]:                             return R.kRed
    if name in ["bkg"]:                             return R.kBlue
    if name in ["qqH","qqH125"]:                    return R.TColor.GetColor(0,100,0)
    if name in ["ggH","ggH125"]:                    return R.TColor.GetColor(0,0,100)
    if name in ["W","jetFakes_W", "w", "W_anti"]:                  return R.TColor.GetColor(222,90,106)
    if name in ["VV","VVJ","VVT", "VVJ_anti", "VVT_anti", "VVL_anti"]:                  return R.TColor.GetColor(175,35,80)
    if name in ["ZL","ZJ","ZLJ", "ZL_anti", "ZJ_anti"]:                   return R.TColor.GetColor(100,192,232)
    if name in ["EWKZ"]:                            return R.TColor.GetColor(8,247,183)
    if name in ["QCD","WSS","jetFakes_QCD", "qcd", "QCD_estimate"]:        return R.TColor.GetColor(250,202,255)
    if name in ["ZTT","DY","real", "ZTT_anti", "EMB_anti"]:                 return R.TColor.GetColor(248,206,104)
    if name in ["jetFakes"]:                        return R.TColor.GetColor(192,232,100)
    if name in ["data"]:                            return R.TColor.GetColor(0,0,0)
    else: return R.kYellow

if __name__ == '__main__':
    main()
