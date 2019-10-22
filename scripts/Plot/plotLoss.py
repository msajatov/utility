import os
import argparse
import cPickle as pickle



modelpath = "/eos/user/m/msajatov/data/storage/nnFractions/output/models/{0}/{1}"


def main():
    

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt','et','tt'], default = 'mt')
    parser.add_argument('-e', dest='era', help='Era',required = True )
    parser.add_argument('-m', dest='mode', help='Mode',required = True )
    
    args = parser.parse_args()
    
    makePlot(args.channel, args.era, ["nn23", "4cat_vars3"])
    
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
    hist1 = pickle.load(open(fullpath0, "rb"))
    
    return [hist0, hist1]
    
def makePlot(channel, era, configs):
    
    for config in configs:
        hist = loadHistory(channel, era, config)
        
        hist0 = hist[0]
        hist1 = hist[1]
    
        loss = hist0["loss"]
        categorical_accuracy = hist0["categorical_accuracy"]
        
        val_loss = hist0["val_loss"]
        val_categorical_accuracy = hist0["val_categorical_accuracy"]
        
        print hist0
        
        print "vca:"
        print val_categorical_accuracy
        
        
        epochs = xrange(1, len(val_loss) + 1)
        
        import matplotlib as mpl
    #     mpl.use('Agg')
        import matplotlib.pyplot as plt
    
        print "plotting training"
        plt.plot(epochs, loss, lw=1, label="Training loss")
        plt.plot(epochs, val_loss, lw=1, label="Validation loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        
    #     plt.plot(epochs, loss, 'b-', val_loss, 'g-')
        plt.show()
    
    
#     filename = "mt_trainHistoryDict_fold_1571342048"

if __name__ == '__main__':
    main()