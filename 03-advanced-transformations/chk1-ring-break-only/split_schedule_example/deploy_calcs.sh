for leg in free bound; do
    for replicate in 1 2 3; do
        JOB_ID=$(sbatch slurm_run_somd2_1.sh $leg $replicate | awk '{print $NF}')
        JOB_ID=$(sbatch slurm_run_somd2_2.sh $leg $replicate | awk '{print $NF}')
        JOB_ID=$(sbatch slurm_run_somd2_3.sh $leg $replicate | awk '{print $NF}')
    done
done
