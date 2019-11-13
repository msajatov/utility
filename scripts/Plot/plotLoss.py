import os
import argparse
import cPickle as pickle
import matplotlib as mpl
    


modelpath = "/eos/user/m/msajatov/data/storage/nnFractions/output/models/{0}/{1}"


def main():
    

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt','et','tt'], default = 'mt')
    parser.add_argument('-e', dest='era', help='Era',required = True )
    
    args = parser.parse_args()
    
    configs = ["nn23", "4cat_vars3"]
    makePlot(args.channel, args.era, configs[0])
    makePlot(args.channel, args.era, configs[1])
    
    makeCombinedPlot(args.channel, args.era, configs)
    
#     loadHistory(args.channel, args.era, args.mode)


def loadHistory(channel, era, config):
    
    dir = modelpath.format(config, era)
    
    files = os.listdir(dir)
    print files
    
    filtered = [f for f in files if "{0}_trainHistoryDict".format(channel) in f]
    print filtered 
    
    if len(filtered) != 2:
        print "Wrong file count"
        return
    
    file0 = filtered[0]
    file1 = filtered[1]
    
    num0 = file0.replace("{0}_trainHistoryDict_fold_".format(channel), "")
    num1 = file1.replace("{0}_trainHistoryDict_fold_".format(channel), "")
    
    if int(num0) > int(num1):
        file_temp = file0
        file0 = file1
        file1 = file_temp
        print "Reversed order"
        
    fullpath0 = os.path.join(dir, file0)
    fullpath1 = os.path.join(dir, file1)
        
    hist0 = pickle.load(open(fullpath0, "rb"))
    hist1 = pickle.load(open(fullpath1, "rb"))
    
    return [hist0, hist1]
    
def makePlot(channel, era, config, suffix=""):
        
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    
    plt.figure()
        
    hist = loadHistory(channel, era, config)       
    
#     maxlength = max(len(hist[0]["val_loss"]), len(hist[1]["val_loss"]))
    
    epochs = xrange(1, len(hist[0]["val_loss"]) + 1)    
    plt.plot(epochs, hist[0]["loss"], lw=1.5, label="Training loss" + suffix)
    plt.plot(epochs, hist[0]["val_loss"], lw=1.5, label="Validation loss" + suffix)
    
#     epochs = xrange(1, len(hist[1]["val_loss"]) + 1)        
#     plt.plot(epochs, hist[1]["loss"], lw=1, label="Training loss" + suffix)
#     plt.plot(epochs, hist[1]["val_loss"], lw=1, label="Validation loss" + suffix)
    
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    
    plt.xlabel("Epoch", fontsize=18)
    plt.ylabel("Loss", fontsize=18)
    plt.legend(fontsize=18)    
    
    fold = 0
    
    plotpath = "plots"
    if not os.path.exists(plotpath):
        os.mkdir(plotpath)
    plt.savefig(os.path.join(plotpath, "{0}_fold_{1}_loss_{2}.png".format(channel, fold, config)), bbox_inches="tight")
    plt.savefig(os.path.join(plotpath, "{0}_fold_{1}_loss_{2}.pdf".format(channel, fold, config)), bbox_inches="tight")
    
#     plt.show()
    
def makeCombinedPlot(channel, era, configs):
    
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    
    plt.figure()
    
    config = configs[0]
    
    hist = loadHistory(channel, era, config)       
    
    epochs = xrange(1, len(hist[0]["val_loss"]) + 1)    

    print "plotting training"
    plt.plot(epochs, hist[0]["loss"], lw=1, label="Training loss (tanh)")
    plt.plot(epochs, hist[0]["val_loss"], lw=1, label="Validation loss (tanh)")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    
    config = configs[1]
    
    hist = loadHistory(channel, era, config)       
    
    epochs = xrange(1, len(hist[0]["val_loss"]) + 1)    

    print "plotting training"
    plt.plot(epochs, hist[0]["loss"], lw=1, label="Training loss (selu)")
    plt.plot(epochs, hist[0]["val_loss"], lw=1, label="Validation loss (selu)")
    plt.legend()
    
    fold = 0
    
    plotpath = "plots"
    if not os.path.exists(plotpath):
        os.mkdir(plotpath)
    plt.savefig(os.path.join(plotpath, "{0}_fold_{1}_loss_{2}.png".format(channel, fold, "combined")), bbox_inches="tight")
    plt.savefig(os.path.join(plotpath, "{0}_fold_{1}_loss_{2}.pdf".format(channel, fold, "combined")), bbox_inches="tight")
    
#     plt.show()
    
    
#     filename = "mt_trainHistoryDict_fold_1571342048"

if __name__ == '__main__':
    main()