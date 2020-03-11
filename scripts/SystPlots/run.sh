VAR=$1

IN_PREFIT=2017_datacard_shapes_prefit.root
IN_POSTFIT=2017_datacard_shapes_postfit_sb.root

python plotSyst.py -i $IN_PREFIT -m 125 -v $VAR -p png -s 1 -l 0 -b -1
python plotSyst.py -i $IN_POSTFIT -m 125 -v $VAR -p png -s 1 -l 0 -b -1

