import Fractions
import subprocess



eras = ["2016",
            "2016_emb"
            "2017",
            "2017_emb"
            ]

eras = [ "2016_emb",
            "2017"
            ]

vars = ["pt_1",
        "pt_2",
        "jpt_1",
        "jpt_2",
        "bpt_1",
        "bpt_2",
        "njets",
        "nbtag",
        "m_sv",
        "mt_1",
        "mt_2",
        "pt_vis",
        "pt_tt",
        "mjj",
        "jdeta",
        "m_vis",
        "dijetpt",
        "met",
        "eta_1",
        "eta_2"
        ]

for era in eras:
    for var in vars:
        args = ["python", "Fractions.py", "--var", var, "-c", "all", "-e", era, "-p"]
        #Fractions.main(args)
        childproc = subprocess.Popen(args)
        op, oe = childproc.communicate()
        childproc.wait()
