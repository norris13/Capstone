#!/bin/bash
#SBATCH -N 1 --ntasks-per-node 1
#SBATCH -t 02:00:00
#SBATCH -p dev_q
#SBATCH -A personal

echo "starting job"

#Record the node that we ran on
echo "Job ran on: $SLURM_NODELIST"

#Load modules


module load Anaconda3/2020.11

#Build. May not be necessary if the program is already built

#Loop over number of threads and run for each
python train_models.py
