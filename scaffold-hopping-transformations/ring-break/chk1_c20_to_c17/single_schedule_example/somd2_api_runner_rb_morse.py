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

    args = parser.parse_args()
    return (
        args.equib_time,
        args.prod_time,
        args.restraints_strength,
        args.system_name,
        args.replicate,
        args.use_hrex,
        args.restart,
        args.extend_time,
        args.ghost_mods,
    )


if __name__ == "__main__":
    (
        equib_time,
        prod_time,
        restraints_strength,
        system_name,
        repl,
        hrex,
        restart,
        extend_time,
        ghost_mods,
    ) = get_user_input()
    logger.info(f"Equilibration Time: {equib_time} picoseconds")
    logger.info(f"Production Time: {prod_time} picoseconds")
    logger.info(f"Restraints Strength: {restraints_strength}")
    logger.info(f"System Name: {system_name}")
    logger.info(f"Replicate: {repl}")
    logger.info(f"Hamiltonian Replica Exchange: {hrex}")
    logger.info(f"Restart: {restart}")
    logger.info(f"Extend Time: {extend_time}")
    logger.info(f"Ghost Modifications: {ghost_mods}")

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


    sire_system = sr.stream.load(f"../prepared_rbfe_input_files/{system_name}.bss")
    ref_system = sire_system.clone()
    ref_system = sr.morph.link_to_reference(ref_system)


    if "chk1_compound_20_to_17" in system_name:
        hard_restraints, sire_system = sr.restraints.morse_potential(
        sire_system,
        de="150 kcal mol-1",
        auto_parametrise=True,
        direct_morse_replacement=True,
        name="morse_hard"
    )
    print(hard_restraints)


    soft_restraints, _ = sr.restraints.morse_potential(
        sire_system,
        atoms0=hard_restraints[0].atom0(),
        atoms1=hard_restraints[0].atom1(),
        r0=hard_restraints[0].r0(),
        k=f"125 kcal mol-1 A-2",
        auto_parametrise=False,
        direct_morse_replacement=False,
        de=f"{restraints_strength} kcal mol-1",
        name="morse_soft",
    )

        logger.debug(f"Restraints: {restraints}")
        selection_string = None

        lambda_values = [
            0.00,
            0.05,
            0.1,
            0.15,
            0.2,
            0.25,
            0.3,
            0.35,
            0.4,
            0.45,
            0.5,
            0.55,
            0.6,
            0.63,
            0.65,
            0.66,
            0.7,
            0.75,
            0.8,
            0.85,
            0.9,
            0.95,
            1.00,
        ]
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


        basename = f"{system_name}_{ghost_mods_name}_repl_{repl}"

        work_dir = f"dynamics/{basename}"

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
        # config.num_energy_neighbours = 2
        if restart:
            config.restart = True
            if extend_time is not None:
                config.runtime = f"{new_prod_time}ps"
            else:
                config.runtime = run_time
        else:
            config.runtime = run_time

        config.lambda_schedule = "ring_break_morph"

        config.equilibration_time = equil_time
        config.equilibration_timestep = equib_timestep
        config.equilibration_constraints = True
        config.energy_frequency = "1ps"
        config.frame_frequency = "20ps"
        config.checkpoint_frequency = "100ps"
        config.save_energy_components = True
        config.restraints = [hard_restraints, soft_restraints]
        config.timeout = "30 s"
        config.lambda_values = lambda_values

        if ghost_mods:
            config.ghost_modifications = True
        else:
            config.ghost_modifications = False
        config.output_directory = work_dir

        if hrex:
            config.replica_exchange = True

            runner = sd.runner.RepexRunner(config=config, system=sire_system)
        else:
            runner = sd.runner.Runner(config=config, system=sire_system)

        runner.run()
