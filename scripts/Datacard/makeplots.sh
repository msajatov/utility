for channel in et mt; do
    for conf in cc cc1 cc2 tt w xx nn13; do
        python plotDatacard.py -c $channel -e 2017 -o $conf -t prefit --syst bpt_1 bpt_2 dijetpt jdeta jpt_1 jpt_2 m_sv m_vis met mjj mt_1 mt_2 nbtag njets pt_1 pt_2 pt_tt pt_vis
        python plotDatacard.py -c $channel -e 2017 -o $conf -t postfit --syst bpt_1 bpt_2 dijetpt jdeta jpt_1 jpt_2 m_sv m_vis met mjj mt_1 mt_2 nbtag njets pt_1 pt_2 pt_tt pt_vis
    done
done

for channel in tt; do
    for conf in cc cc1 cc2 tt w xx nn13a; do
        python plotDatacard.py -c $channel -e 2017 -o $conf -t prefit --syst bpt_1 bpt_2 dijetpt jdeta jpt_1 jpt_2 m_sv m_vis met mjj mt_1 mt_2 nbtag njets pt_1 pt_2 pt_tt pt_vis
        python plotDatacard.py -c $channel -e 2017 -o $conf -t postfit --syst bpt_1 bpt_2 dijetpt jdeta jpt_1 jpt_2 m_sv m_vis met mjj mt_1 mt_2 nbtag njets pt_1 pt_2 pt_tt pt_vis
    done
done

