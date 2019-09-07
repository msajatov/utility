import pandas
import root_pandas as rp
from Sample import Sample
import root_numpy as rn
import ROOT as R
from ROOT import TFile

class DataReader:

    def __init__(self):
        pass

    def get_data_for_sample(self, sample, columns=""):
        path = sample.full_path
        where = sample.cut.getForDF()
        
        tmp = rp.read_root(paths=path,
                           where=where,
                           columns=columns,
                           chunksize=None)

        return tmp

    def get_data_frame(self, path, where, columns):
        tmp = rp.read_root(paths=path,
                           where=where,
                           columns=columns,
                           chunksize=None)

        return tmp

    def get_iterator(self, path, where, columns, chunksize):
        tmp = rp.read_root(paths=path,
                           where=where,
                           columns=columns,
                           chunksize=chunksize)

        return tmp
    
    def get_root_tree(self, sample):
        path = sample.full_path
        
        tfile1 = R.TFile(path, "read")  
        #tfile1.Close()
        return tfile1

