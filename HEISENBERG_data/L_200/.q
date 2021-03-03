#!/bin/zsh
source ~/.zshrc
for nw in 100 1000 10000 100000;
do
cat >>input_$nw<<EOF
      read_dmc
      nw$nw.dat
      100
      5
      100
      quit
EOF
qmcino<input_$nw
mv dmc_en.dat L200_nw$nw.dat
done
