from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import pandas as pd
import os

class ensemble_net:
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

        model_0_path = os.path.join(saved_models_dir, 'model_10_n1_8.h5')
        model_1_path = os.path.join(saved_models_dir, 'model_1_n1_8.h5')
        model_2_path = os.path.join(saved_models_dir, 'model_2_n1_8.h5')
        model_3_path = os.path.join(saved_models_dir, 'model_3_n1_8.h5')
        model_4_path = os.path.join(saved_models_dir, 'model_4_n1_8.h5')
        model_5_path = os.path.join(saved_models_dir, 'model_5_n1_8.h5')
        model_6_path = os.path.join(saved_models_dir, 'model_6_n1_8.h5')
        model_7_path = os.path.join(saved_models_dir, 'model_7_n1_8.h5')
        model_8_path = os.path.join(saved_models_dir, 'model_8_n1_8.h5')
        model_9_path = os.path.join(saved_models_dir, 'model_9_n1_8.h5')

        # Load all the models
        model_0 = keras.models.load_model(model_0_path, compile = False)
        model_1 = keras.models.load_model(model_1_path, compile = False)
        model_2 = keras.models.load_model(model_2_path, compile = False)
        model_3 = keras.models.load_model(model_3_path, compile = False)
        model_4 = keras.models.load_model(model_4_path, compile = False)
        model_5 = keras.models.load_model(model_5_path, compile = False)
        model_6 = keras.models.load_model(model_6_path, compile = False)
        model_7 = keras.models.load_model(model_7_path, compile = False)
        model_8 = keras.models.load_model(model_8_path, compile = False)
        model_9 = keras.models.load_model(model_9_path, compile = False)

        inputs = keras.Input(shape=(384,))

        # Define each sub model
        y0 = model_0(inputs)
        y1 = model_1(inputs)
        y2 = model_2(inputs)
        y3 = model_3(inputs)
        y4 = model_4(inputs)
        y5 = model_5(inputs)
        y6 = model_6(inputs)
        y7 = model_7(inputs)
        y8 = model_8(inputs)
        y9 = model_9(inputs)

        # Finally generate ensemble model
        ml_corrs = [y0, y1, y2, y3, y4, y5, y6, y7, y8, y9]
        outputs = layers.average([y0, y1, y2, y3, y4, y5, y6, y7, y8, y9])

        print(f"Loaded ensemble {atom_type}")

        return keras.Model(inputs=inputs, outputs=([outputs,ml_corrs]))

    def calc_dml_nmr(self, config):
        count = 0
        working_directory = config["Processing"]["data_path"]


        for filename in sorted(os.listdir(working_directory)):
            if filename.endswith('.aev'):
                # print(filename)
                dml_file = filename[:-4] + ".dml"
                cheap_shielding_file = filename[:-4] + ".shifts"

                aev_path = os.path.join(working_directory, filename)
                cheap_shielding_path = os.path.join(working_directory, cheap_shielding_file)
                dml_path = os.path.join(working_directory, dml_file)

                cheap_shieldings = pd.read_csv(cheap_shielding_path, header=None)
                data = pd.read_csv(aev_path, header=None)
                data['cheap'] = cheap_shieldings
                # Need next line in case there is only 1 atom
                # to avoid 0-D data
                # aev = aev.reshape((-1, 384))

                H_data = data[data[0] == 1]
                if not H_data.empty:
                    H_aev = H_data.iloc[:, 1:385]
                    ensemble_ml_corrs_H = self.H_net.predict(H_aev)
                    ensemble_ml_corrs_H = np.asarray(ensemble_ml_corrs_H)

                    if config['Processing']['dft'] == 'aev':
                        H_data['aev'] = ensemble_ml_corrs_H[0]
                        H_data['std'] = np.std(ensemble_ml_corrs_H[1], axis=0)
                    else:
                        H_data['dml'] = H_data['cheap'] + ensemble_ml_corrs_H[0][:,0]
                        H_data['std'] = np.std(ensemble_ml_corrs_H[1], axis=0)


                C_data = data[data[0] == 6]
                if not C_data.empty:
                    C_aev = C_data.iloc[:, 1:385]
                    ensemble_ml_corrs_C = self.C_net.predict(C_aev)
                    ensemble_ml_corrs_C = np.asarray(ensemble_ml_corrs_C)

                    if config['Processing']['dft'] == 'aev':
                        C_data['aev'] = ensemble_ml_corrs_C[0]
                        C_data['std'] = np.std(ensemble_ml_corrs_C[1], axis=0)
                    else:
                        C_data['dml'] = C_data['cheap'] + ensemble_ml_corrs_C[0][:,0]
                        C_data['std'] = np.std(ensemble_ml_corrs_C[1], axis=0)


                N_data = data[data[0] == 7]
                if not N_data.empty:
                    N_aev = N_data.iloc[:, 1:385]
                    ensemble_ml_corrs_N = self.N_net.predict(N_aev)
                    ensemble_ml_corrs_N = np.asarray(ensemble_ml_corrs_N)

                    if config['Processing']['dft'] == 'aev':
                        N_data['aev'] = ensemble_ml_corrs_N[0]
                        N_data['std'] = np.std(ensemble_ml_corrs_N[1], axis=0)
                    else:
                        N_data['dml'] = N_data['cheap'] + ensemble_ml_corrs_N[0][:,0]
                        N_data['std'] = np.std(ensemble_ml_corrs_N[1], axis=0)

                O_data = data[data[0] == 8]
                if not O_data.empty:
                    O_aev = O_data.iloc[:, 1:385]
                    ensemble_ml_corrs_O = self.O_net.predict(O_aev)
                    ensemble_ml_corrs_O = np.asarray(ensemble_ml_corrs_O)

                    if config['Processing']['dft'] == 'aev':
                        O_data['aev'] = ensemble_ml_corrs_O[0]
                        O_data['std'] = np.std(ensemble_ml_corrs_O[1], axis=0)
                    else:
                        O_data['dml'] = O_data['cheap'] + ensemble_ml_corrs_O[0][:,0]
                        O_data['std'] = np.std(ensemble_ml_corrs_O[1], axis=0)

                data = pd.concat([H_data, C_data, N_data, O_data], sort=False).sort_index()

                if config['Processing']['dft'] == 'aev':
                    dml = data['aev']
                else:
                    dml = data['dml']
                std = data['std']

                shifts = np.array([dml, std]).T
                np.savetxt(dml_path, shifts, fmt="%1.5f")
                count += 1

        if count == 0:
            print(f'No AEV files found in {working_directory}\nexiting...')
            exit()