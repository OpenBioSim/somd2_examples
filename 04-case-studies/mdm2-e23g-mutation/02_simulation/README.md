Now that we have built a perturbable SOMD2 system file, we have 3 different options for running the simulation and defining the run parameters.
1. We can simply pass the parameters using the SOMD2 CLI, by simply running `somd2 mdm2_e23g_open_conf_am7209.bss --some-parameter`, see `somd2 -h` for all possible CLI options.
2. We can use a SOMD2 config `.yaml` file that will tell SOMD2 how we want to run the simulation. The config file will overwrite any default values that would be used by SOMD2. We can then pass this config file into CLI and keep a file-based record of how we configured the simulation.
3. We can use SOMD2 Python API - This provides the greatest amount of flexibility in terms of setup, however this is also the most low-level approach.

> [!Important]
> Whatever approach you use to run a SOMD2 simulation, remember to let SOMD2 know what GPU(s) you have available by using `CUDA_VISIBLE_DEVICES` environment variable.
> E.g `export CUDA_VISIBLE_DEVICES=0,1,2,3` in a quad-GPU setup. This isn't necessary when using SLURM as it will normally do this automatically for you.

In this tutorial we will use approach 2., the [config_short_run.yaml](config_short_run.yaml) contains an example config file that overwrites some of the SOMD2 defaults (note that some of the config parameters are default anyway, like `num_lambda: 11` for example):
- `runtime: 500 ps` sets up a short simulation production time for testing.
- `ghost_modifications: false` disables default ghost atom modifications (currently experimental).
- `replica_exchange: true` enables a HREX simulation that will use all declared GPUs simultaneously.
- `shift_coulomb: "1 A"` and `shift_delta: "1.5 A"` control the soft-core parameters.

```bash
somd2 mdm2_e23g_open_conf_am7209.bss --config config_short_run.yaml
```

In the terminal output we will see that SOMD2 has detected a net charge change and has added an alchemical co-ion for us automatically. 

```python
2026-06-26 17:09:21.164 | INFO     | somd2.runner._base:__init__:366 - There is a charge difference of 1 between the end states. Adding alchemical ions to keep the charge constant.
2026-06-26 17:09:21.284 | DEBUG    | somd2.runner._base:_create_alchemical_ions:1154 - Found Cl- ion in system.
2026-06-26 17:09:21.287 | INFO     | somd2.runner._base:_create_alchemical_ions:1263 - Water at molecule index 1994 will be perturbed to a Cl- ion to keep charge constant.
```
> [!Caution]
> `--charge-difference` option controls what SOMD2 does in terms of charge-changing transformations. If you pass the `--charge-difference 0` to SOMD2, it will not setup a co-alchemical ion in the simulation even if the perturbation contains a net charge-change. If the user does not specify anything, SOMD2 will automatically add alchemical ions to balance the charge throughout the transformation.

> [!Tip]
> SOMD2 can setup a distance restraint between the co-alchemical ion and the COM of the perturbable molecule if needed to prevent them interacting.
> See `--coalchemical-restraint-dist` option for more details.

When the simulation is complete, head over to the [03_analysis](../03_analysis/) to analyse the simulation results.