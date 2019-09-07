import json
import sys
from Sample import Sample
from TargetCategory import TargetCategory
from common.Tools.CutObject.CutObject import Cut
import os


def main():
    cp = ConfigParser("mt", 2017, "conf/frac_config_mt_2017.json")


class ConfigParser:

    def __init__(self, channel, era, file_path):
        
        filepath = os.path.dirname(os.path.realpath(__file__))
        
        Cut.cutfile = os.path.join(filepath, "conf/cuts_{0}.json".format(era))
        
        self.channel = channel
        self.era = era
        self.file_path = file_path

        self.samples = []
        self.target_categories = []
        self.variable_names = []
        self.additional_variable_names = []
        self.weights = []
        self.lumi = 0

        self.data_root_path = ""

        self.cut_dict = {}

        self.cut_config_path = os.path.join(filepath, "conf/cuts_{0}.json".format(era))
        self.read_cut_mapping(self.cut_config_path)
        self.parse(self.file_path)

    def parse(self, path):
        # parse config and return boolean to indicate success
        try:
            with open(path,"r") as FSO:
                config = json.load(FSO)
        except ValueError as e:
            print e
            print "Check {0}. Probably a ',' ".format(path)
            sys.exit(0)

        self._parse_data_root_path(config)
        self._parse_lumi(config)
        self._parse_weights(config)
        self._parse_variable_names(config)
        self._parse_additional_variable_names(config)
        self._parse_categories(config)
        self._parse_sample(config)

        self._add_samples_to_categories()

        #for cat in self.target_categories:
            #print cat.name + ":"
            #for sset in cat.samples:
                #print sset
            #print "\n"

    def read_cut_mapping(self, cut_config_path):
        with open(cut_config_path, "r") as FSO:
            cuts = json.load(FSO)
            for c in cuts:
                cuts[c] = self._assert_channel(cuts[c])
            self.cut_dict = cuts

    def get_sample_sets(self):
        return self.samples

    def get_target_categories(self):
        return self.target_categories

    def get_target_names(self):
        target_names = {}
        for cat in self.target_categories:
            target_names[cat.index] = cat.name
        return target_names

    def get_target_name_list(self):
        return [cat.name for cat in self.target_categories]

    def _parse_categories(self, config):
        print "Parsing categories..."
        cat = TargetCategory("none", 1)
        cat.index = -1
        self.target_categories.append(cat)

        for key in config["class_weight"]:
            val = config["class_weight"][key]
            name = key
            class_weight = self._assert_channel(val)
            target_cat = TargetCategory(name, class_weight)
            print target_cat
            self.target_categories.append(target_cat)

        #print self.target_categories

        for i, target_cat in enumerate(self.target_categories):
            for key in config["target_values"]:
                val = config["target_values"][key]
                if key == target_cat.get_name():
                    prob_index = self._assert_channel(val)
                    target_cat.index = prob_index

    def _parse_sample(self, config):
        #print "Parsing sample sets..."
        for key in config["samples"]:
            val = config["samples"][key]
            # this is not the full file path yet! (training vs. prediction?)
            source = self._assert_channel(val["name"])
            source_name = "{0}-{1}.root".format(self.channel, source)
            target_name = self._assert_channel(val["target"])
            # make this return a list of Cut instances? Only if Cut class can be implemented properly
            cuts = self._parse_cut(val["select"])
            
            cutObject = self._parse_cutObject(val["select"])
            
            event_weight = self._assert_channel(val["event_weight"])
            eff_weight = self._getEffWeight(event_weight, key)

            categories = [c for c in self.target_categories if c.name == target_name]

            if len(categories) != 1:
                raise ValueError("Target category not found or ambiguous!")

            category = categories[0]

            sample_set = Sample(key, source_name, cutObject, category, event_weight, eff_weight)
            sample_set.full_path = os.path.join(self.data_root_path, sample_set.source_file_name)

            self.samples.append(sample_set)

            #print sample_set

            # check if target is one of the valid, defined ones
            # for training: check if target is not the default one (none)

    def _parse_variable_names(self, config):
        print "Parsing variable names..."
        self.variable_names = self._assert_channel(config["variables"])

    def _parse_additional_variable_names(self, config):
        print "Parsing additional variable names..."
        self.additional_variable_names = self._assert_channel(config["addvar"])

        for v in config["shifted_variables"]:
            # if v in self.config["shifted_variables"]:
                self.additional_variable_names.append(v+"*")

    def _parse_lumi(self, config):
        self.lumi = config["lumi"]

    def _parse_weights(self, config):
        self.weights = config["weights"]

    def _getEffWeight(self, event_weight, sample_name):
        if type(event_weight) is list:
            if "EMB" in sample_name:
                lumi = 1.0
            else:
                lumi = self.lumi
            return "*".join(event_weight + [str(lumi)])

        if type(event_weight) is float:
            return str(event_weight)

        if type(event_weight) is unicode:
            if "EMB" in sample_name:
                lumi = 1.0
            else:
                lumi = self.lumi
            return "*".join([event_weight, str(lumi)])

        else:
            return 1.0

    def _parse_data_root_path(self, config):
        path = config["path"]
        if self.era == "2016":
            path = path.format(self.channel)
        self.data_root_path = path

    def _add_samples_to_categories(self):
        for cat in self.target_categories:
            sample_sets = [sample for sample in self.samples if sample.target.name == cat.name]
            cat.samples = sample_sets

    def _assert_channel(self, entry):
        if type(entry) is dict:
            return entry[self.channel]
        else:
            return entry

    def _parse_cut(self, cutstring):
        cutstring = self._assert_channel(cutstring)
        for alias, cut in self.cut_dict.items():
            cutstring = cutstring.replace(alias, cut)
        return cutstring
    
    def _parse_cutObject(self, cutstring):
        cutstring = self._assert_channel(cutstring)
        C = Cut(cutstring, self.channel)
        return C

if __name__ == '__main__':
    main()
