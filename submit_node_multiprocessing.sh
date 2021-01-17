#!/bin/bash -l

#SBATCH -o ./job.out.%j
#SBATCH -e ./job.err.%j
#SBATCH -D ./
#SBATCH -J PYTHON_MP
#SBATCH --mail-type=none
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1   # only start 1 task via srun because Python multiprocessing starts more tasks internally
#SBATCH --cpus-per-task=32    # assign all the cores to that first task to make room for Python's multiprocessing tasks
#SBATCH --time=00:01:00

module purge
module load anaconda/3

# avoid overbooking of the cores which might occur via NumPy/MKL threading
export OMP_NUM_THREADS=1

echo "stating job ..."
python ./python_multiprocessing.py $SLURM_CPUS_PER_TASK

echo "...done"