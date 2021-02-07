#!/bin/bash -l

#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J PYTHON_MP
#SBATCH --mail-user=cecile.aprili@gmail.com
#SBATCH --mail-type=begin
#SBATCH --mail-type=end
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1   
#SBATCH --cpus-per-task=16
#SBATCH --time=00:01:00
#SBATCH --mem=42G
#SBATCH --error=memo_test.%J.err
#SBATCH --output=memo_test.%J.py

module purge
module load anaconda/3

export OMP_NUM_THREADS=1

python ./run.py $SLURM_CPUS_PER_TASK