for nw in 100 1000 10000 100000 1000000;
do
cat >>inputPlot_$nw<<EOF
    read_dmc
    data_$nw
    100
    5
    100
    quit
EOF
python3 qmcino.py <inputPlot_$nw
mv dmc_en.dat L10_nw$nw.dat
done

