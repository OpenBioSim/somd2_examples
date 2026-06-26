for leg in free bound; do
    for replicate in 1 2 3; do
        sbatch slurm_run_somd2.sh $leg $replicate
    done
done
