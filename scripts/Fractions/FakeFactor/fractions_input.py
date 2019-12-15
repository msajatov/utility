from Tools.CutObject.CutObject import Cut
from Tools.Weights.Weights import Weight

class Era:

    def __init__(self, era, channel, shift="NOMINAL"):

        if era == "2016":
            # Cut.cutfile = "/afs/hephy.at/work/m/mspanring/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2016/cuts.json"
            Cut.cutfile = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2016/cuts.json"
            self.lumi = 35.87
            self.weights = "puweight * stitchedWeight * trk_sf * genweight * effweight * topWeight_run1 * zPtReweightWeight * antilep_tauscaling"
            self.tauidsfs = {
                "tight":  "0.95",
                "vtight": "0.93"
            }

            self.add_weights = self.weights.replace(" ","").split("*")
            path = "/afs/hephy.at/data/higgs01/data_2016/ntuples_v6/{0}/ntuples_SVFIT_merged/{0}-{1}_ntuple_".format(
                channel, shift)
            mc_path = path.format(channel, shift)
            data_path = path.format(channel, "NOMINAL")

            self.mcSamples = [
                (mc_path + "WJets.root", "W", ""),
                (mc_path + "DY.root", "ZTT", Cut("-GENTAU-")),
                (mc_path + "DY.root", "ZL", Cut("!(-GENTAU- | -GENJET-)")),
                (mc_path + "DY.root", "ZJ", Cut("-GENJET-")),
                (mc_path + "TT.root", "TTT", Cut("-GENTAU-")),
                (mc_path + "TT.root", "TTL", Cut("!(-GENTAU- | -GENJET-)")),
                (mc_path + "TT.root", "TTJ", Cut("-GENJET-")),
                (mc_path + "VV.root", "VVT", Cut("-GENTAU-")),
                (mc_path + "VV.root", "VVL", Cut("!(-GENTAU- | -GENJET-)")),
                (mc_path + "VV.root", "VVJ", Cut("-GENJET-")),
            ]

            self.dataSample = data_path + "Data.root"

        if era == "2016_emb":
            # Cut.cutfile = "/afs/hephy.at/work/m/mspanring/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2016/cuts.json"
            Cut.cutfile = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2016/cuts.json"
            self.lumi = 35.87
            self.weights = "puweight * stitchedWeight * trk_sf * genweight * effweight * topWeight_run1 * zPtReweightWeight * antilep_tauscaling"
            self.tauidsfs = {
                "tight":  "0.95",
                "vtight": "0.93"
            }

            self.add_weights = self.weights.replace(" ", "").split("*")
            path = "/afs/hephy.at/data/higgs01/data_2016/ntuples_v6/{0}/ntuples_SVFIT_merged/{0}-{1}_ntuple_".format(channel, shift)
            mc_path = path.format(channel, shift)
            data_path = path.format(channel, "NOMINAL")

            self.mcSamples = [
                (mc_path + "WJets.root", "W", ""),
                (mc_path + "EMB.root", "EMB", Cut("-GENTAU-")),
                # (mc_path + "DY.root","ZTT",Cut("-GENTAU-") ),
                (mc_path + "DY.root", "ZL", Cut("!(-GENTAU- | -GENJET-)")),
                (mc_path + "DY.root", "ZJ", Cut("-GENJET-")),
                # (mc_path + "TT.root","TTT",Cut("-GENTAU-") ),
                (mc_path + "TT.root", "TTL", Cut("!(-GENTAU- | -GENJET-)")),
                (mc_path + "TT.root", "TTJ", Cut("-GENJET-")),
                # (mc_path + "VV.root","VVT",Cut("-GENTAU-") ),
                (mc_path + "VV.root", "VVL", Cut("!(-GENTAU- | -GENJET-)")),
                (mc_path + "VV.root", "VVJ", Cut("-GENJET-")),
            ]
            self.dataSample = data_path + "Data.root"

        if era == "2016_pred":
            Cut.cutfile = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2016/cuts.json"
            self.lumi = 35.87
            self.weights = "weight"
            self.tauidsfs = {
                "tight":  "0.95",
                "vtight": "0.93"
            }

            self.add_weights = self.weights.replace(" ","").split("*") 
            path = "/afs/hephy.at/data/mspanring01/predictions/{0}-".format( channel)
            ext = ".root"

            self.mcSamples = [
                (path + shift + "_ntuple_W"+ext,"W",""),
                (path + shift + "_ntuple_DY"+ext,"ZTT",Cut("-GENTAU-") ),
                (path + shift + "_ntuple_DY"+ext,"ZL", Cut("!(-GENTAU- | -GENJET-)") ),
                (path + shift + "_ntuple_DY"+ext,"ZJ", Cut("-GENJET-") ),
                (path + shift + "_ntuple_TT"+ext,"TTT",Cut("-GENTAU-") ),
                (path + shift + "_ntuple_TT"+ext,"TTL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + shift + "_ntuple_TT"+ext,"TTJ",Cut("-GENJET-") ),
                (path + shift + "_ntuple_VV"+ext,"VVT",Cut("-GENTAU-") ),
                (path + shift + "_ntuple_VV"+ext,"VVL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + shift + "_ntuple_VV"+ext,"VVJ",Cut("-GENJET-") ),
            ]
            self.dataSample = path + "NOMINAL_ntuple_Data"+ext

        if era == "2016_pred_emb":
            Cut.cutfile = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2016/cuts.json"
            self.lumi = 35.87
            self.weights = "weight"
            self.tauidsfs = {
                "tight":  "0.95",
                "vtight": "0.93"
            }

            self.add_weights = self.weights.replace(" ","").split("*") 
            path = "/afs/hephy.at/data/mspanring01/predictions_2016/{0}-".format( channel)
            ext = ".root"

            self.mcSamples = [
                (path + shift + "_ntuple_W"+ext,"W",""),
                (path + shift + "_ntuple_EMB"+ext,"EMB",Cut("-GENTAU-") ),
                # (path + shift + "_ntuple_DY"+ext,"ZTT",Cut("-GENTAU-") ),
                (path + shift + "_ntuple_DY"+ext,"ZL", Cut("!(-GENTAU- | -GENJET-)") ),
                (path + shift + "_ntuple_DY"+ext,"ZJ", Cut("-GENJET-") ),
                # (path + shift + "_ntuple_TT"+ext,"TTT",Cut("-GENTAU-") ),
                (path + shift + "_ntuple_TT"+ext,"TTL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + shift + "_ntuple_TT"+ext,"TTJ",Cut("-GENJET-") ),
                # (path + shift + "_ntuple_VV"+ext,"VVT",Cut("-GENTAU-") ),
                (path + shift + "_ntuple_VV"+ext,"VVL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + shift + "_ntuple_VV"+ext,"VVJ",Cut("-GENJET-") ),
            ]
            self.dataSample = path + "NOMINAL_ntuple_Data"+ext

        if era == "2017":
            Cut.cutfile = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2017/cuts.json"
            self.lumi = 41.529
            self.weights = "weight*zPtReweightWeight*topPtReweightWeightRun1"
            
            self.tauidsfs = {
                "tight":  "0.89",
                "vtight": "0.86"
            }
            if channel == "tt": self.weights += "*sf_DoubleTauTight"
            else: self.weights += "*sf_SingleXorCrossTrigger"
            
            self.add_weights = self.weights.replace(" ","").split("*")

            path = "/afs/hephy.at/data/higgs01/v10/{0}-{1}_ntuple_".format( channel, shift)
            self.mcSamples = [
                (path + "WJets.root","W",""),
                (path + "DY.root","ZTT",Cut("-GENTAU-") ),
                (path + "DY.root","ZL", Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "DY.root","ZJ", Cut("-GENJET-") ),
                (path + "TT.root","TTT",Cut("-GENTAU-") ),
                (path + "TT.root","TTL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "TT.root","TTJ",Cut("-GENJET-") ),
                (path + "VV.root","VVT",Cut("-GENTAU-") ),
                (path + "VV.root","VVL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "VV.root","VVJ",Cut("-GENJET-") ),
            ]
            self.dataSample = path + "Data.root"

        if era == "2017_emb":
            Cut.cutfile = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2017/cuts.json"
            self.lumi = 41.529
            self.weights = "weight*zPtReweightWeight*topPtReweightWeightRun1"
            
            self.tauidsfs = {
                "tight":  "0.89",
                "vtight": "0.86"
            }
            if channel == "tt": self.weights += "*sf_DoubleTauTight"
            else: self.weights += "*sf_SingleXorCrossTrigger"
            
            self.add_weights = self.weights.replace(" ","").split("*")

            path = "/afs/hephy.at/data/higgs01/v10/{0}-{1}_ntuple_".format( channel, shift)
            self.mcSamples = [
                (path + "WJets.root","W",""),
                (path + "EMB.root","EMB",Cut("-GENTAU-") ),                
                # (path + "DY.root","ZTT",Cut("-GENTAU-") ),
                (path + "DY.root","ZL", Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "DY.root","ZJ", Cut("-GENJET-") ),
                # (path + "TT.root","TTT",Cut("-GENTAU-") ),
                (path + "TT.root","TTL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "TT.root","TTJ",Cut("-GENJET-") ),
                # (path + "VV.root","VVT",Cut("-GENTAU-") ),
                (path + "VV.root","VVL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "VV.root","VVJ",Cut("-GENJET-") ),
            ]
            self.dataSample = path + "Data.root"

        if era == "2017_pred":
            Cut.cutfile = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2017/cuts.json"
            self.lumi = 41.529
            self.weights = "weight*zPtReweightWeight*topPtReweightWeightRun1"
            
            self.tauidsfs = {
                "tight":  "0.89",
                "vtight": "0.86"
            }
            if channel == "tt": self.weights += "*sf_DoubleTauTight"
            else: self.weights += "*sf_SingleXorCrossTrigger"
            
            self.add_weights = self.weights.replace(" ","").split("*")

            path = "/afs/hephy.at/data/mspanring01/predictions_2017/{0}-{1}_ntuple_".format( channel, shift)
            self.mcSamples = [
                (path + "WJets.root","W",""),
                (path + "DY.root","ZTT",Cut("-GENTAU-") ),
                (path + "DY.root","ZL", Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "DY.root","ZJ", Cut("-GENJET-") ),
                (path + "TT.root","TTT",Cut("-GENTAU-") ),
                (path + "TT.root","TTL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "TT.root","TTJ",Cut("-GENJET-") ),
                (path + "VV.root","VVT",Cut("-GENTAU-") ),
                (path + "VV.root","VVL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "VV.root","VVJ",Cut("-GENJET-") ),
            ]
            self.dataSample = path + "Data.root"

        if era == "2017_pred_emb":
            Cut.cutfile = "/afs/hephy.at/work/m/msajatovic/CMSSW_9_4_0/src/HephyHiggs/Tools/Datacard/conf2017/cuts.json"
            self.lumi = 41.529
            self.weights = "weight*zPtReweightWeight*topPtReweightWeightRun1"
            
            self.tauidsfs = {
                "tight":  "0.89",
                "vtight": "0.86"
            }
            if channel == "tt": self.weights += "*sf_DoubleTauTight"
            else: self.weights += "*sf_SingleXorCrossTrigger"
            
            self.add_weights = self.weights.replace(" ","").split("*")

            path = "/afs/hephy.at/data/mspanring01/predictions_2017/{0}-{1}_ntuple_".format( channel, shift)
            self.mcSamples = [
                (path + "W.root","W",""),
                (path + "EMB.root","EMB",Cut("-GENTAU-") ),                
                # (path + "DY.root","ZTT",Cut("-GENTAU-") ),
                (path + "DY.root","ZL", Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "DY.root","ZJ", Cut("-GENJET-") ),
                # (path + "TT.root","TTT",Cut("-GENTAU-") ),
                (path + "TT.root","TTL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "TT.root","TTJ",Cut("-GENJET-") ),
                # (path + "VV.root","VVT",Cut("-GENTAU-") ),
                (path + "VV.root","VVL",Cut("!(-GENTAU- | -GENJET-)") ),
                (path + "VV.root","VVJ",Cut("-GENJET-") ),
            ]
            self.dataSample = path + "Data.root"