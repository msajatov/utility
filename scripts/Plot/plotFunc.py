import os
import argparse
import cPickle as pickle
import matplotlib as mpl
import numpy as np


# modelpath = "/eos/user/m/msajatov/data/storage/nnFractions/output/models/{0}/{1}"
modelpath = "/eos/user/m/msajatov/data/storage/nn/models/{0}/{1}"

def sigmoid(x):
    return (1 / (1 + np.exp(-x)))

def relu(x):
    zero = np.zeros(len(x))
    return np.max([zero, x], axis=0)

def selu(x):
    alpha = 1.6732632423543772848170429916717
    scale = 1.0507009873554804934193349852946
    return scale * ((x > 0)*x + (x <= 0) * (alpha * np.exp(x) - alpha))

def elu(x):
    alpha = 1.6732632423543772848170429916717
    return ((x > 0)*x + (x <= 0) * (alpha * np.exp(x) - alpha))

def main():   

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', dest='channel', help='Decay channel' ,choices = ['mt','et','tt'], default = 'mt')
    parser.add_argument('-e', dest='era', help='Era')
    parser.add_argument('-m', dest='mode', help='Mode',default = '' )
    
    args = parser.parse_args()    
    
    makePlot(["sigmoid", "tanh"])
    makePlot(["ReLU", "SELU"])
    makePlot(["ReLU"])
    makePlot(["ELU"])
    makePlot(["SELU"])
    
def makePlot(functionnames):
        
    mpl.use('Agg')
    import matplotlib.pyplot as plt
    
    #plt.set_cmap("Greys")
    plt.rcParams['image.cmap'] = 'Greys'
    fig = plt.figure(facecolor='w', figsize=(6,4))

    ax = fig.add_subplot(1,1,1) 
    ax.grid(which='major', axis='both', linestyle='-', color='lightgrey')    
    
    colormap=["lightgrey", "grey", "black"]

    for i, fname in enumerate(functionnames):
        arrays = getArrays(fname, plt)        
        plt.plot(arrays[0], arrays[1], lw=1.5, label=fname, c=colormap[len(colormap) - len(functionnames) + i])
    
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    
    plt.xlabel("x", fontsize=18)
    plt.ylabel("h(x)", fontsize=18)
    plt.legend(fontsize=18, loc="upper left")   
    
    plotpath = "plots"
    if not os.path.exists(plotpath):
        os.mkdir(plotpath)
    name = ""
    for fname in functionnames:
        name += fname + "_"
    plt.savefig(os.path.join(plotpath, "{0}.png".format(name)), bbox_inches="tight")
    
    #plt.show()

def getArrays(functionname, plt):

    if functionname == "tanh":
        plt.ylim(-1.1, 1.1)  
        in_array = np.linspace(-6, 6, 50) 
        out_array = np.tanh(in_array)
    elif functionname == "sigmoid":
        plt.ylim(-1.1, 1.1)  
        in_array = np.linspace(-6, 6, 50) 
        out_array = sigmoid(in_array)
    elif functionname == "ReLU":
        plt.ylim(-2.5, 10.5)  
        in_array = np.linspace(-10, 10, 50) 
        out_array = relu(in_array)
    elif functionname == "SELU":
        plt.ylim(-2.5, 10.5)   
        in_array = np.linspace(-10, 10, 50) 
        out_array = selu(in_array)
    elif functionname == "ELU":
        plt.ylim(-2.5, 10.5)   
        in_array = np.linspace(-10, 10, 50) 
        out_array = elu(in_array)

    return [in_array, out_array]


    
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