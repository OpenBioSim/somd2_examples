import argparse
import sire as sr
import somd2 as sd
import os
from shutil import copy2
from loguru import logger


def get_user_input():
    parser = argparse.ArgumentParser(description="Simulation parameters")
    parser.add_argument(
        "--equib_time",
        type=int,
        required=True,
        help="Equilibration time in picoseconds",
    )
    parser.add_argument(
        "--prod_time", type=int, required=True, help="Production time in picoseconds"
    )
    parser.add_argument(
        "--restraints_strength", type=str, required=True, help="Restraints strength (De value)"
    )
    parser.add_argument("--system_name", type=str, required=True, help="System to run")
    parser.add_argument("--schedule_stage", type=int, required=True, help="Schedule stage to run")
    parser.add_argument(
        "--replicate",
        type=int,
        required=False,
        help="Replicate to run. If not provided, all replicates will be run",
    )
    parser.add_argument(
        "--use_hrex",
        action="store_true",
        help="Whether to run a Hamiltonian replica exchange simulation",
    )
    parser.add_argument(
        "--use_rest2",
        action="store_true",
        help="Whether to run a REST2 simulation",
    )

    parser.add_argument(
        "--bond_strength",
        type=float,
        required=True,
        help="Bond strength for the restraints",
    )

    parser.add_argument(
        "--restart",
        action="store_true",
        help="Whether to restart the simulation from a previous checkpoint",
    )

    parser.add_argument(
        "--extend_time",
        type=int,
        required=False,
        help="Time to extend the simulation by",
    )

    parser.add_argument(
        "--ghost_mods",
        action="store_true",
        help="Whether to use ghosts atom modifications in the simulation",
    )

    parser.add_argument(
        "--rest2_scale",
        type=int,
        required=False,
        help="REST2 scaling factor",
    )
    parser.add_argument(
        "--focused_sampling",
        action="store_true",
        help="Whether to use focused sampling in the simulation",
    )

    args = parser.parse_args()
    return (
        args.equib_time,
        args.prod_time,
        args.restraints_strength,
        args.system_name,
        args.schedule_stage,
        args.replicate,
        args.use_hrex,
        args.use_rest2,
        args.bond_strength,
        args.restart,
        args.extend_time,
        args.ghost_mods,
        args.rest2_scale,
        args.focused_sampling,
    )


if __name__ == "__main__":
    (
        equib_time,
        prod_time,
        restraints_strength,
        system_name,
        schedule_stage,
        repl,
        hrex,
        rest2,
        k,
        restart,
        extend_time,
        ghost_mods,
        rest2_scale,
        focused_sampling,
    ) = get_user_input()
    logger.info(f"Equilibration Time: {equib_time} picoseconds")
    logger.info(f"Production Time: {prod_time} picoseconds")
    logger.info(f"Restraints Strength: {restraints_strength}")
    logger.info(f"System Name: {system_name}")
    logger.info(f"Schedule Stage: {schedule_stage}")
    logger.info(f"Replicate: {repl}")
    logger.info(f"Hamiltonian Replica Exchange: {hrex}")
    logger.info(f"REST2: {rest2}")
    logger.info(f"Bond Strength: {k}")
    logger.info(f"Restart: {restart}")
    logger.info(f"Extend Time: {extend_time}")
    logger.info(f"Ghost Modifications: {ghost_mods}")
    logger.info(f"REST2 Scaling Factor: {rest2}")
    logger.info(f"Focused Sampling: {focused_sampling}")

    if extend_time is not None:
        if restart is False:
            logger.error(
                "You cannot extend the production time if you are not restarting the simulation!"
            )
            raise ValueError("Restart must be True to extend production time.")

        new_prod_time = prod_time + extend_time
        logger.info(
            f"Extending production time by {extend_time} ps to {new_prod_time} ps"
        )


    if not rest2_scale:
        rest2_scale = 1

    sire_system = sr.stream.load(f"../prepared_rbfe_input_files/{system_name}.bss")
    ref_system = sire_system.clone()
    ref_system = sr.morph.link_to_reference(ref_system)


    if "chk1_compound_20_to_17" in system_name:
        restraints = sr.restraints.morse_potential(
        sire_system,
        k=f"{k} kcal mol-1 A-2",
        de=f"{restraints_strength} kcal mol-1",
        auto_parametrise=True,
    )

        logger.debug(f"Restraints: {restraints}")
        selection_string = None

        # morph 10
        if schedule_stage == 1:
            lambda_values = [
                0.00,
                0.01,
                0.02,
                0.03,
                0.05,
                0.1,
                0.2,
                0.33,
                0.4,
                0.8,
                1.00,
            ]

        elif schedule_stage == 2:
            lambda_values = [
                0.00,
                0.1,
                0.20,
                0.3,
                0.40,
                0.5,
                0.60,
                0.7,
                0.80,
                0.9,
                0.95,
                0.97,
                1.00,
            ]

        elif schedule_stage == 3:
            lambda_values = [
                0.00,
                0.05,
                0.1,
                0.20,
                0.3,
                0.40,
                0.5,
                0.60,
                0.7,
                0.80,
                0.9,
                0.95,
                1.00,
            ]
   

        basename_modifier = None
    else:
        logger.info("No restraints defined for this system")
        raise NotImplementedError

    # DYANMICS PARAMETERS
    if repl is None:
        repls = [1, 2, 3]
    else:
        repls = [repl]

    for repl in repls:

        equil_time = f"{equib_time}ps"
        run_time = f"{prod_time}ps"
        equib_timestep = "1fs"
        dt = "2fs"

        if ghost_mods:
            ghost_mods_name = "ghost_mods"
        else:
            ghost_mods_name = "no_ghosts"

        if basename_modifier == None:
            basename_modifier = ""
        else:
            basename_modifier = f"{basename_modifier}"

        basename = f"{system_name}_{ghost_mods_name}_morse_ring_break_stage_{schedule_stage}_{restraints_strength}_de_{int(k)}_k_morse_potential_restr_{basename_modifier}_repl_{repl}"

        if hrex:
            work_dir = f"dynamics_hrex/{basename}"
            if rest2:
                work_dir = f"dynamics_rest2/{basename}"
        else:
            work_dir = f"dynamics_std/{basename}"

        # check if work_dir exists, if not create it
        if not os.path.exists(work_dir):
            os.makedirs(work_dir)
        else:
            logger.info(
                f"Directory {work_dir} already exists, cleaning it in the next step!"
            )

        # delete the old directory matching the same name
        if not restart:
            if not os.path.exists(work_dir):
                os.makedirs(work_dir)
            else:
                os.system(f"rm -r {work_dir}")

        config = sd.config.Config()

        ### SOMD2 CONFIGURATION
        config.log_level = "debug"
        config.log_file = "output.log"
        config.cutoff = "12A"
        config.cutoff_type = "PME"
        config.timestep = dt
        config.num_energy_neighbours = 2
        if restart:
            config.restart = True
            if extend_time is not None:
                config.runtime = f"{new_prod_time}ps"
            else:
                config.runtime = run_time
        else:
            config.runtime = run_time

        config.lambda_schedule = f"morse_ring_break_morph_10_split_{schedule_stage}"

        config.equilibration_time = equil_time
        config.equilibration_timestep = equib_timestep
        config.equilibration_constraints = True
        config.multi_conformational_seeding = False
        config.energy_frequency = "1ps"
        # config.frame_frequency = "20ps"
        config.frame_frequency = "100ps"
        config.checkpoint_frequency = "100ps"
        config.save_energy_components = True
        config.restraints = restraints
        config.timeout = "30 s"
        config.lambda_values = lambda_values
        config.lambda_energy = lambda_values

        if ghost_mods:
            config.ghost_modifications = True
        else:
            config.ghost_modifications = False
        config.output_directory = work_dir

        if focused_sampling:
            config.focused_sampling_lambda_range = [0.7, 1.0]

        if hrex:
            config.replica_exchange = True
            config.oversubscription_factor = 1

            if rest2:
                config.rest2_scale = rest2_scale
                config.rest2_selection = selection_string

            runner = sd.runner.RepexRunner(config=config, system=sire_system)
        else:
            runner = sd.runner.Runner(config=config, system=sire_system)

        runner.run()

        try:
            logger.info("Copying topology files")
            copy2(f"{work_dir}/system0.prm7", f"{work_dir}/system0.parm7")
            copy2(f"{work_dir}/system1.prm7", f"{work_dir}/system1.parm7")
        except FileNotFoundError:
            logger.info("Could not find the topology files to copy")
            pass
