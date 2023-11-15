#!/bin/bash

# allocate run resources
export NUMEXPR_MAX_THREADS=8
export CUDA_VISIBLE_DEVICES=0

# control multiple GPU allocation
multi_GPU=false

if [ $multi_GPU = true ]; then
	export CUDA_VISIBLE_DEVICES=0,1,2,3
fi

# free leg (ligand only)
cd free || exit
somd2 ejm31-ejm50.bss --log-level trace

# bound leg (protein + ligand)
cd ../bound || exit
somd2 ejm31-ejm50.bss --log-level trace
