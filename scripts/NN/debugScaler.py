import os
import argparse
import cPickle

def main():
    scaler_filepath = "test/StandardScaler.et.pkl"
    if os.path.exists(scaler_filepath):
        print "Loading Scaler"
        with open(scaler_filepath, "rb") as FSO:
            scaler = cPickle.load(FSO)
            print "loading successful"
            print "scaler: " + str(scaler)
            print "mean: " + str(scaler.mean_)
            print "var: " + str(scaler.var_)
            print "n_samples_seen: " + str(scaler.n_samples_seen_)
            print "scale: " + str(scaler.scale_)
    else:
        print "Fatal: Scaler file not found at {0}. Train model using -t first.".format(
            scaler_filepath)
        return


if __name__ == '__main__':
    main()