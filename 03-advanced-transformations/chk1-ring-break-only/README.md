# Overview

- [prepared_rbfe_input_files](prepared_rbfe_input_files/) contains SOMD2 ready perturbable run files.
- [create_perturbed_system](create_perturbed_system.ipynb) details how input files were generated from raw inputs.
- [single_schedule_example](single_schedule_example/) shows SOMD2 run protocols for both Morse and Auxiliary restraints.

# Run Instructions

```bash
cd single_schedule_example
./launch_calcs.sh
```

For Auxiliary restraints calculation, uncomment the relevant part of the [slurm script](single_schedule_example/slurm_run_somd2.sh) and run same as above.
Experimentally determined $\Delta \Delta G$ for this transformation is: -0.51 kcal/mol.

Bound leg dG (triplicate): -33.83 +/- 0.10 kcal/mol   
Free leg dG (triplicate): -33.76 +/- 0.01 kcal/mol   
