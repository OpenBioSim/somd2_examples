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
restraints_strength=50
bond_strength=125
system_name=chk1_compound_20_to_17_"$leg"
rest2_scale=1

# Morse potential for bond breaking

echo "Running somd2 leg=\"$leg\" replicate=\"$replicate\""

# run first job with specified schedule, attempting to rerun if it fails
# python3 somd2_api_runner_rb_morse.py --prod_time "$prod_time" \
#                                --equib_time "$equib_time" \
#                                --restraints_strength "$restraints_strength" \
#                                --bond_strength "$bond_strength" \
#                                --system_name "$system_name" \
#                                --use_hrex \
#                                --use_rest2 \
#                                --rest2_scale "$rest2_scale" \
#                                --replicate "$replicate"

# # make sure sampling is fully complete if a crash occurs
# for i in {1..5};
# do
#     python3 somd2_api_runner_rb_morse.py --prod_time "$prod_time" \
#                                --equib_time "$equib_time" \
#                                --restraints_strength "$restraints_strength" \
#                                --bond_strength "$bond_strength" \
#                                --system_name "$system_name" \
#                                --use_hrex \
#                                --use_rest2 \
#                                --rest2_scale "$rest2_scale" \
#                                --replicate "$replicate" \
#                                --restart
# done

# For auxiliary restraints, we don't pass bond_strength, as we use a different script
restraints_strength=10

echo "Running somd2 leg=\"$leg\" replicate=\"$replicate\""

# run first job with specified schedule, attempting to rerun if it fails
python3 somd2_api_runner_rb_auxiliary.py --prod_time "$prod_time" \
                               --equib_time "$equib_time" \
                               --restraints_strength "$restraints_strength" \
                               --system_name "$system_name" \
                               --use_hrex \
                               --use_rest2 \
                               --rest2_scale "$rest2_scale" \
                               --replicate "$replicate"

for i in {1..5};
do
    python3 somd2_api_runner_rb_auxiliary.py --prod_time "$prod_time" \
                               --equib_time "$equib_time" \
                               --restraints_strength "$restraints_strength" \
                               --system_name "$system_name" \
                               --use_hrex \
                               --use_rest2 \
                               --rest2_scale "$rest2_scale" \
                               --replicate "$replicate" \
                               --restart
done