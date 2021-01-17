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
#SBATCH --cpus-per-task=20    
#SBATCH --time=00:01:00
#SBATCH --mem=42G
#SBATCH --error=JobName.%J.err
#SBATCH --output=JobName.%J.out

module purge
module load anaconda/3

export OMP_NUM_THREADS=1

echo "stating job ..."
python ./python_multiprocessing.py $SLURM_CPUS_PER_TASK

echo "...done"