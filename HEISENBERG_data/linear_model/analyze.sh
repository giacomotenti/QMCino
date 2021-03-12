#!/bin/zsh
source ~/.zshrc
for nw in 100 1000 10000 100000 1000000;
do
cat >>input_$nw<<EOF
      linear
      read_dmc
      nw$nw.dat
      100
      5
      100
      quit
EOF
qmcino<input_$nw
mv dmc_en.dat linear_nw$nw.dat
done
