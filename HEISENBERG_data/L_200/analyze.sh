#!/bin/zsh
source ~/.zshrc
for nw in 1000000;
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
