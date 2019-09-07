import json
import pandas as pd
import numpy as np


def loadDF():
    
    path = "output/complete_metrics.json"
    metrics = load(path)
    
    # [model][channel][var]
    
    rows_list = []     
    for metricskey, metricsval in metrics.items():
        for modelkey, modelval in metricsval.items():
            for channelkey, channelval in modelval.items():
                for varkey, varval in channelval.items():                    
                    new_row = {'metric':metricskey, 'model':modelkey, 'var':varkey, 'channel':channelkey, 'qcd':varval["qcdx"], 'real':varval["realx"], 'tt':varval["ttx"], 'w':varval["wx"], 'completeMetric':varval}
                    rows_list.append(new_row)
                    
            
    df = pd.DataFrame(rows_list, columns=["metric", "model", "var", "channel", "qcd", "real", "tt", "w", "completeMetric"])  
    
    df.eval("total = qcd + tt + w")
    
    return df    
    
def compareSideBySide(df, configs, channel="mt", metric="diff"):  
        
    filtered = df.drop("completeMetric", axis=1)
    filtered = filtered.drop("qcd", axis=1)
    filtered = filtered.drop("real", axis=1)
    filtered = filtered.drop("tt", axis=1)
    filtered = filtered.drop("w", axis=1)
    
    subset = filtered.query("channel == '{0}'".format(channel))   \
                .query("metric == '{0}'".format(metric))                    
        
    subset = subset.sort_values(by=["var", "model"])
    
    confdf = subset.query("model == '{0}'".format(configs[0]))
    confdf = confdf.rename(columns = {"total":configs[0]})
    confdf = confdf.drop("model", axis=1)   
    
    result = confdf
    
    for conf in configs[1:]: 
        confdf = subset.query("model == '{0}'".format(conf))
        confdf = confdf.rename(columns = {"total":conf})
        confdf = confdf.drop("model", axis=1)   
        #print confdf            
        
        result = pd.merge(result, confdf, on=["var", "channel"])
        
    #printWithStyle(result)
    #applyStyle(result)
    return result


def load(path):
    try:
        with open(path, "r") as FSO:
            data = json.load(FSO)
    except ValueError as e:
        print e
        print "ValueError while parsing data"
        return
    except IOError as e:
        print "IOError while parsing data"
        print e
        return
    return data


if __name__ == '__main__':
    main()