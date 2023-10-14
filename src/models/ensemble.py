from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pandas as pd
import os


class EnsembleNet:
    def __init__(self, config):
        self.path = config["Processing"]["model_path"]
        self.H_net = None
        self.C_net = None
        self.N_net = None
        self.O_net = None
        self.load_weight_by_atom_type()

    def load_weight_by_atom_type(self):
        self.H_net = self.load_weights("1H")
        self.C_net = self.load_weights("13C")
        self.N_net = self.load_weights("15N")
        self.O_net = self.load_weights("17O")

    def load_weights(self, atom_type):
        saved_models_dir = os.path.join(self.path, atom_type)

        model_paths = [
            os.path.join(saved_models_dir, f"model_{i}_n1_8.h5") for i in range(10)
        ]

        # Load all the models
        models = [
            keras.models.load_model(model_path, compile=False)
            for model_path in model_paths
        ]

        inputs = keras.Input(shape=(384,))

        # Define each sub model
        ml_corrs = [model(inputs) for model in models]

        # Finally generate ensemble model
        outputs = layers.average(ml_corrs)

        print(f"Loaded ensemble {atom_type}")

        return keras.Model(inputs=inputs, outputs=([outputs, ml_corrs]))

    def calc_dml_nmr(self, config):
        count = 0
        working_directory = config["Processing"]["data_path"]

        for filename in sorted(os.listdir(working_directory)):
            if filename.endswith(".aev"):
                dml_file = filename[:-4] + ".dml"
                cheap_shielding_file = filename[:-4] + ".shifts"

                aev_path = os.path.join(working_directory, filename)
                cheap_shielding_path = os.path.join(
                    working_directory, cheap_shielding_file
                )
                dml_path = os.path.join(working_directory, dml_file)

                cheap_shieldings = pd.read_csv(cheap_shielding_path, header=None)
                data = pd.read_csv(aev_path, header=None)
                data["cheap"] = cheap_shieldings

                H_data = data[data[0] == 1]
                if not H_data.empty:
                    H_aev = H_data.iloc[:, 1:385]
                    ensemble_ml_corrs_H = self.H_net.predict(H_aev)
                    ensemble_ml_corrs_H = np.asarray(ensemble_ml_corrs_H)

                    if config["Processing"]["dft"] == "aev":
                        H_data["aev"] = ensemble_ml_corrs_H[0]
                        H_data["std"] = np.std(ensemble_ml_corrs_H[1], axis=0)
                    else:
                        H_data["dml"] = H_data["cheap"] + ensemble_ml_corrs_H[0][:, 0]
                        H_data["std"] = np.std(ensemble_ml_corrs_H[1], axis=0)

                C_data = data[data[0] == 6]
                if not C_data.empty:
                    C_aev = C_data.iloc[:, 1:385]
                    ensemble_ml_corrs_C = self.C_net.predict(C_aev)
                    ensemble_ml_corrs_C = np.asarray(ensemble_ml_corrs_C)

                    if config["Processing"]["dft"] == "aev":
                        C_data["aev"] = ensemble_ml_corrs_C[0]
                        C_data["std"] = np.std(ensemble_ml_corrs_C[1], axis=0)
                    else:
                        C_data["dml"] = C_data["cheap"] + ensemble_ml_corrs_C[0][:, 0]
                        C_data["std"] = np.std(ensemble_ml_corrs_C[1], axis=0)

                N_data = data[data[0] == 7]
                if not N_data.empty:
                    N_aev = N_data.iloc[:, 1:385]
                    ensemble_ml_corrs_N = self.N_net.predict(N_aev)
                    ensemble_ml_corrs_N = np.asarray(ensemble_ml_corrs_N)

                    if config["Processing"]["dft"] == "aev":
                        N_data["aev"] = ensemble_ml_corrs_N[0]
                        N_data["std"] = np.std(ensemble_ml_corrs_N[1], axis=0)
                    else:
                        N_data["dml"] = N_data["cheap"] + ensemble_ml_corrs_N[0][:, 0]
                        N_data["std"] = np.std(ensemble_ml_corrs_N[1], axis=0)

                O_data = data[data[0] == 8]
                if not O_data.empty:
                    O_aev = O_data.iloc[:, 1:385]
                    ensemble_ml_corrs_O = self.O_net.predict(O_aev)
                    ensemble_ml_corrs_O = np.asarray(ensemble_ml_corrs_O)

                    if config["Processing"]["dft"] == "aev":
                        O_data["aev"] = ensemble_ml_corrs_O[0]
                        O_data["std"] = np.std(ensemble_ml_corrs_O[1], axis=0)
                    else:
                        O_data["dml"] = O_data["cheap"] + ensemble_ml_corrs_O[0][:, 0]
                        O_data["std"] = np.std(ensemble_ml_corrs_O[1], axis=0)

                data = pd.concat(
                    [H_data, C_data, N_data, O_data], sort=False
                ).sort_index()

                if config["Processing"]["dft"] == "aev":
                    dml = data["aev"]
                else:
                    dml = data["dml"]
                std = data["std"]

                shifts = np.array([dml, std]).T
                np.savetxt(dml_path, shifts, fmt="%1.5f")
                count += 1

        if count == 0:
            print(f"No AEV files found in {working_directory}\nexiting...")
            exit()
