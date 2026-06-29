import argparse
import somd2 as sd
from somd2.config import Config
import sire as sr


def get_user_input():
    parser = argparse.ArgumentParser(description="Simulation parameters")
    parser.add_argument(
        "--replicate",
        type=int,
        required=True,
        help="Replicate to run.",
    )
    parser.add_argument(
        "--bond_strength",
        type=str,
        required=False,
        help="Bond strength for soft morse potential. If not provided, a default value of 125 kcal/mol/A^2 will be used",
        default=125,
    )
    parser.add_argument("--de_strength", type=str, required=True, help="DE strength for soft morse potential.")
    args = parser.parse_args()
    return (
        args.de_strength,
        args.replicate,
        args.bond_strength,
    )


def main():
    (
        de_strength,
        replicate,
        bond_strength,
    ) = get_user_input()

    somd2_config = Config()
    somd2_config.lambda_values = [
        0.0,
        0.05,
        0.1,
        0.2,
        0.3,
        0.33,
        0.34,
        0.4,
        0.5,
        0.6,
        0.65,
        0.7,
        0.75,
        0.8,
        0.85,
        0.9,
        0.95,
        1.0,
    ]

    sire_system = sr.stream.load(f"OMTKY3-L18P.bss")

    somd2_config.lambda_schedule = "reverse_ring_break_morph"

    hard_restraints, sire_system = sr.restraints.morse_potential(
        sire_system,
        de="150 kcal mol-1",
        auto_parametrise=True,
        direct_morse_replacement=True,
        name="morse_hard",
    )
    print(hard_restraints)

    soft_restraints, _ = sr.restraints.morse_potential(
        sire_system,
        atoms0=hard_restraints[0].atom0(),
        atoms1=hard_restraints[0].atom1(),
        r0=hard_restraints[0].r0(),
        k=f"{bond_strength} kcal mol-1 A-2",
        auto_parametrise=False,
        de=f"{de_strength} kcal mol-1",
        name="morse_soft",
    )
    print(soft_restraints)
    somd2_config.restraints = [hard_restraints, soft_restraints]


    somd2_config.output_directory = (
        f"OMTKY3-L18P_k_{int(bond_strength)}_de_{int(de_strength)}_repl_{replicate}"
    )
    somd2_config.equilibration_time = f"500ps"
    somd2_config.runtime = "500ps"
    somd2_config.frame_frequency = "10ps"
    somd2_config.checkpoint_frequency = f"500ps"

    somd2_config.equilibration_timestep = "2fs"
    somd2_config.energy_frequency = "1ps"
    somd2_config.cutoff = "10A"
    somd2_config.cutoff_type = "PME"
    somd2_config.ghost_modifications = False

    somd2_config.equilibration_constraints = True
    somd2_config.num_energy_neighbours = 5
    somd2_config.h_mass_factor = 3
    somd2_config.rest2_scale = 1
    somd2_config.replica_exchange = True
    somd2_config.log_level = "debug"
    somd2_config.save_xml = True

    somd2_config.timeout = "30s"
    somd2_config.shift_delta = "1.5A"
    somd2_config.shift_coulomb = "1A"

    runner = sd.runner.RepexRunner(config=somd2_config, system=sire_system)
    runner.run()


if __name__ == "__main__":
    main()