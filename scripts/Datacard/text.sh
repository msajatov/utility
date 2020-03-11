conf=$1
type=$2
p_sat=$3
p_KS=$4
p_AD=$5
r=$6


convert -font helvetica -fill black -pointsize 20 \
-draw "text 420,300 '$conf'" \
-draw "text 420,320 '$type" \
-draw "text 420,340 '$p_sat'" \
-draw "text 420,360 '$p_KS'" \
-draw "text 420,380 '$p_AD'" \
-draw "text 420,400 '$r'" \
test.png out.png