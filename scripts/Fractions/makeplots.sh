CONF=$1

for CH in et mt tt
do
    for NUM in 0 1 2 3
    do
	python plotFractions.py -c $CH -e 2017 predicted_frac_prob_${NUM}
    done
done

mkdir /eos/user/m/msajatov/wormhole/tempoutput/distribution/${CONF}
mv /eos/user/m/msajatov/wormhole/tempoutput/new/distribution/* /eos/user/m/msajatov/wormhole/tempoutput/distribution/${CONF}/