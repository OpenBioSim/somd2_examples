#!/bin/bash
#SBATCH -o somd2.%j.slurm.out
#SBATCH -n 32
#SBATCH --gres=gpu:4
#SBATCH --job-name=somd2

export NUMEXPR_MAX_THREADS=32

leg=$1
replicate=$2

# calc params

prod_time=5000
equib_time=250
schedule_stage=2
restraints_strength=125
bond_strength=50
system_name=chk1_compound_20_to_17_"$leg"
rest2_scale=1

echo "Running somd2 leg=\"$leg\" replicate=\"$replicate\""

# run first job with specified schedule, attempting to rerun if it fails
python3 somd2_api_runner_rb_split.py --prod_time "$prod_time" --equib_time "$equib_time" --schedule_stage "$schedule_stage" --restraints_strength "$restraints_strength" --bond_strength "$bond_strength" --system_name "$system_name" --use_hrex --use_rest2 --rest2_scale "$rest2_scale" --replicate "$replicate" || python3 somd2_api_runner_rb_split.py --prod_time "$prod_time" --equib_time "$equib_time" --schedule_stage "$schedule_stage" --restraints_strength "$restraints_strength" --bond_strength "$bond_strength" --system_name "$system_name" --use_hrex --use_rest2 --rest2_scale "$rest2_scale" --replicate "$replicate"

# make sure sampling is fully complete
for i in {1..10};
do
    python3 somd2_api_runner_rb_split.py --prod_time "$prod_time" --equib_time "$equib_time" --schedule_stage "$schedule_stage" --restraints_strength "$restraints_strength" --bond_strength "$bond_strength" --system_name "$system_name" --use_hrex --use_rest2 --rest2_scale "$rest2_scale" --replicate "$replicate" --restart
done