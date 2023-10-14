import re
import os
import torch
import torchani
import numpy as np
from ase.io import read, write
import string


def process_data(config):
    if config["Processing"]["reprocess_shieldings"]:
        get_shieldings_from_log(config)
    if config["Processing"]["reprocess_aev"]:
        gen_aev(config)


def get_shieldings_from_log(config):
    # nmr_dict = {"13C": "C", "1H": "H", "15N": "N", "17O": "O"}
    print("Generating Shift files...")
    search_term = "    Isotropic"
    pattern = re.compile(search_term)

    for filename in sorted(os.listdir(config["Processing"]["data_path"])):
        if filename.endswith(".log"):
            shift_file = os.path.join(
                config["Processing"]["data_path"], filename[:-4] + ".shifts"
            )

            path = os.path.join(config["Processing"]["data_path"], filename)
            with open(path, "r") as f:
                with open(shift_file, "w") as sf:
                    for line in f:
                        match = re.search(pattern, line)
                        if match:
                            shieldings = line.split()
                            sf.write(shieldings[4])
                            sf.write("\n")


def gen_aev(config):
    device = torch.device("cpu")

    model = torchani.models.ANI1ccx()
    path = config["Processing"]["data_path"]
    print("Generating AEV files...")

    for filename in sorted(os.listdir(path)):
        if filename.endswith(".log"):
            file = os.path.join(path, filename)
            # print(file)

            # Read in molecule using ASE
            molecule = read(file)

            # Atom codes for ANI code
            atoms = model.species_to_tensor(molecule.symbols).to(device).unsqueeze(0)
            coords = torch.tensor(
                [molecule.get_positions()], requires_grad=False, device=device
            )

            # Generate AEV
            _, aev = model.aev_computer((atoms, coords))

            # HCNO atoms
            atoms = molecule.get_atomic_numbers()
            atoms.astype(int)

            final_aev = np.column_stack(
                (molecule.get_atomic_numbers(), aev.data.cpu().numpy()[0])
            )

            # Save AEV
            aev_file = filename[:-3] + "aev"
            aev_file_path = os.path.join(path, aev_file)
            # print(final_aev)
            np.savetxt(aev_file_path, final_aev, fmt=",".join(["%i"] + ["%1.8E"] * 384))
