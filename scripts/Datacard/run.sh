channel=et
era=2017
var=m_vis
conf=w

# make plot
python plotDatacard.py -c $channel -e $era $var -o $conf --syst

# retrieve p values, r etc.
python getData.py -c $channel -e $era $var -o $conf

# write over png
python writeText.py -i temp.txt -o ${conf}_${era}_plots/htt_${channel}_100_Run2017_prefit_${var}_ff_EMB.png 