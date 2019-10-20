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


    args = parser.parse_args()
    Datacard.use_config = "conf" +  args.era

    for u in args.var:
        if not args.plot_only:
            makeDatacard(args.channel, u, args.out, args.era, args.real_est, args.syst, args.debug, args.fake_est, args.prefix)

        if args.out:
            makePlot(args.channel, u, args.out, args.era, "{0}_{1}_plots".format(args.out, args.era))
        else:
            makePlot(args.channel, u, args.out, args.era)
        #input = raw_input("Enter any key to exit parent: ")

def makePlot(channel, variable, indir, era, outdir = ""):
    var = Var(variable)

    if "2016" in era: lumi = "35.9"
    if "2017" in era: lumi = "41.5"

    if indir:  root_datacard = "/".join([indir, "htt_{0}.inputs-sm-Run{1}-{2}.root".format(channel, era,var.name) ])
    else:
        root_datacard = "{0}/htt_{1}.inputs-sm-Run{2}-{3}.root".format("_".join([era, "datacards"]), channel, era, var.name)
    file = R.TFile(root_datacard)

    for category in file.GetListOfKeys():
        cat = category.GetName()
        interesting_ones = {}
        for h in ["W","VVT","VVL","VVJ","TTT","TTL","TTJ","ZTT","ZL","ZJ", "QCD",
                 "jetFakes","jetFakes_W","jetFakes_TT","jetFakes_QCD","EMB","data_obs"]:

            if h == "data_obs":
                interesting_ones["data"] = copy.deepcopy( file.Get("{0}/{1}".format(cat,h) ) )
            else:
                interesting_ones[h] = copy.deepcopy( file.Get("{0}/{1}".format(cat,h)  ) )
        

        plots = [ ("_def",["W","VVT","VVL","VVJ","TTT","TTL","TTJ","ZTT","ZL","ZJ","QCD","data"]),
                  ("_def_EMB",["W","VVL","VVJ","TTL","TTJ","EMB","ZL","ZJ","QCD","data"]),
                  ("_ff",["VVT","VVL","TTT","TTL","ZTT","ZL","jetFakes","data"]),
                  ("_ff_split",["VVT","VVL","TTT","TTL","ZTT","ZL","jetFakes_W","jetFakes_TT","jetFakes_QCD","data"]),
                  ("_ff_EMB_split",["VVL","TTL","ZL","EMB","jetFakes_W","jetFakes_TT","jetFakes_QCD","data"]),
                  ("_ff_EMB",["VVL","TTL","EMB","ZL","jetFakes","data"])
        ]
        for p in plots:
            histos = {}
            plot = True
            for h in p[1]:
                if type(interesting_ones[h]) == R.TObject: plot = False
                histos[h] = interesting_ones[h]
            if not outdir:
                outdir = "_".join([era, "plots/"])

            if plot: pl.plot(histos, canvas="semi", signal = [], descriptions = {"plottype": "ProjectWork", "xaxis":var.tex, "channel":channel,"CoM": "13", "lumi":lumi  }, outfile = outdir +"/"+ cat+"_"+var.name + p[0] +".png" )
    file.Close() 