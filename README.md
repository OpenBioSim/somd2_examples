# SOMD2 Examples & Tutorials

A collection of [SOMD2](https://github.com/OpenBioSim/somd2/) input files and end-to-end tutorials showcasing the capabilities of SOMD2. 

This repository is organized by **progression and complexity**. If you are looking for a specific type of transformation (e.g., charge-changing, ring-breaking, or covalent bonding), please refer to the **Directory Table** below.

---

## Directory Table

Use this table to find the exact tutorial or example system that matches the chemical transformation you want to run.

**Status Legend:**
* 🟢 **Full Tutorial** (End-to-End: `01_setup`, `02_simulation`, `03_analysis`)
* 🟡 **System Only** (Ready-to-run `.bss` file provided, no analysis scripts)
* 🔴 **WIP** (Work in Progress)

| Transformation Concept | Target System | Directory Path | Status |
| :--- | :--- | :--- | :--- |
| **Basic Charge-Change (Validation)** | Sodium (Na+ → Na°) | [`01-basics/sodium-in-a-box`](./01-basics/sodium-in-a-box) | 🟡
| **Standard Ligand RBFE** | TYK2 | [`02-standard-rbfe/tyk2-ejm31-to-ejm50`](./02-standard-rbfe/tyk2-ejm31-to-ejm50) | 🟡
| **Covalent RBFE** | hCatL | [`03-advanced-transformations/hCatL-covalent`](./03-advanced-transformations/hCatL-covalent) | 🟡
| **Protein Sidechain Mutation** | MDM2 | [`03-advanced-transformations/mdm2-v14g-protein-mutation`](./03-advanced-transformations/mdm2-v14g-protein-mutation) | 🟡
| **Scaffold Hopping (Ring-Break)** | CHK1 | [`03-advanced-transformations/chk1-ring-break-only`](./03-advanced-transformations/chk1-ring-break-only) | 🟡
| **Charge-Changing Mutation** | MDM2 | [`04-case-studies/mdm2-e23g-mutation`](./04-case-studies/mdm2-e23g-mutation) | 🟢
| **Proline Mutation** | OMTKY3 | [`04-case-studies/OMTKY3-proline-mutation`](./04-case-studies/OMTKY3-proline-mutation) | 🟢

---

## Internal Folder Structure

To keep workflows reproducible and clean, every full tutorial in this repository will aim to adhere to a three-phase internal folder structure. This separates system preparation, simulation execution, and data analysis.

Inside a tutorial directory, you will find:

### `01_setup/`
Contains the initial structural files (e.g., raw `.pdb`, `.sdf`, `.mol2` files) and the Python scripts used to prepare the system. 

### `02_simulation/`
Shows how to run the SOMD2 simulation for the specific use-case. 

### `03_analysis/`
Shows how to process the SOMD2 results generated in the simulation section.

---

## Dependencies

Running these examples **requires the devlopment (`devel`) versions** of OpenBioSim software stack (see https://github.com/OpenBioSim/somd2#installation for details). Check individual tutorial `README` files for specific version requirements.

> [!Caution]
> If you are getting segmentation faults when running BioSimSpace free energy analysis code, this is most likely due to the `jax` library that was pulled in during the installation process. `jax` is a depedency of `PyMBAR` and `alchemlyb` which BioSimSpace uses to carry out MBAR analysis. In this case, downgrading the CPU-build of `jax` should resolve all problems:
> ```bash
> conda install "jaxlib=*=*cpu*" jax -c conda-forge --force-reinstall
> ```