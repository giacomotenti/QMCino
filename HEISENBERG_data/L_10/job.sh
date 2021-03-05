for nw in 100 1000 10000 100000;
do
cat >>input_$nw<<EOF
      set_param
      10
      dmc
      10000
      5
      $nw
      
      quit
EOF
python3 qmcino.py<input_$nw
mv dmc_heis.dat data_$nw
done
