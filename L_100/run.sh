for i in  100 1000 10000 100000 1000000
do
dldir="$i.nw"
[ ! -d "$dldir" ] && mkdir -p "$dldir"
cd $i.nw

cat >> qmc.in << EOF
set_param
100
dmc
10000
5
$i
q
EOF
cat>>submit.job<<EOF
#!/bin/bash
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=32
#SBATCH --cpus-per-task=1
##SBATCH --mem=180000
#SBATCH --time=11:59:59
#SBATCH --partition=regular2
#SBATCH --job-name=dmc$i
#SBATCH --mail-user=drigo96@live.it
#SBATCH --mail-type=ALL

#umask -S u=rwx,g=r,o=r


# Define number of processors to send to mpirun for MPICH
NNODES=2




NPROCS=\$((NNODES*32))
cd \${SLURM_SUBMIT_DIR}
echo \$SLURM_SUBMIT_DIR


echo "\$(date)"
export OMP_NUM_THREADS=2

python3 ../qmcino.py<qmc.in
echo " Done."

EOF
sbatch submit.job
cd ../
done
