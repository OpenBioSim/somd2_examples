# SOMD2 Examples

Collection of [SOMD2](https://github.com/OpenBioSim/somd2/) input files showcasing SOMD2 FEP capabilities.

Examples
========

## Full Tutorials
Full tutorials aim to detail the end-to-end process of an example of SOMD2 transformation run. This covers:
1. Generation of perturbable systems from raw inputs (pdb, sdf files for example).
2. Specific run SOMD2 run procedures.
3. Result analysis.

* [`scaffold-hopping-transformations`](ligand-rbfe/scaffold-hopping-transformations/ring-break/chk1_c20_to_c17) - Example of a ligand RBFE scaffold-hopping transformation

## Example Perturbable SOMD2 Systems
Example perturbable systems do not contain setup details or SOMD2 run procedures, these are just SOMD2 binary `.bss` meant for rapid distribution and testing of advanced use cases, such as covalent mutations or testing of charge-changing transformations.
* [`noncovalent-rbfe`](ligand-rbfe/tyk2) - Standard RBFE calculation for TYK2.
* [`sidechain-mutations`](protein-fep/non-covalent-rbfe/mdm2/v14g) - Mutation between two canonical amino acid sidechains for MDM2.
* [`covalent-rbfe`](protein-fep/covalent-rbfe/hCatL) - RBFE calculation between two covalently bound ligands for hCatL.
* [`sodium-in-a-box`](sodium-in-a-box) - Sodium charge changing (Na+ --> Na°) calculation.