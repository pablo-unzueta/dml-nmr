import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from math import sqrt
import os
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from tensorflow.keras.wrappers.scikit_learn import KerasRegressor
import re
import subprocess

class ensemble_net:
    def __init__(self, atom, directory, dft='PBE0', basis_set='6-31G', std=False):
        self.atom_type = atom
        self.dft = dft
        self.basis_set = basis_set
        self.std = std
        self.working_directory = directory
        self.saved_models_dir = self.determine_weights_directory()
        #self.model = self.load_weights()

    def determine_weights_directory(self):
        dft_dir = self.dft
        basis_set_dir = self.basis_set

        dft_dir = dft_dir.lower()
        basis_set_dir = basis_set_dir.lower()
        basis_set_dir = basis_set_dir.replace('-','')

        atom_dict = {'C' : '13C',
                     'H' : '1H',
                     'N' : '15N',
                     'O' : '17O'}

        return "../saved_nets/" + dft_dir + "_" + basis_set_dir + "/" + atom_dict[self.atom_type]



    def load_weights(self):
        saved_models_dir = self.saved_models_dir

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
        return keras.Model(inputs=inputs, outputs=([outputs,ml_corrs]))

    #def predict_shieldings(self):

    def get_shieldings(self):

        search_term = self.atom_type + "    Isotropic"

        pattern = re.compile(search_term)

        for filename in sorted(os.listdir(self.working_directory)):
            if filename.endswith('.log'):
                shift_file = filename[:-4] + ".shift"

                with open(filename, 'r') as f:
                    with open(shift_file, 'w') as sf:
                        for line in f:
                            match = re.search(pattern, line)
                            if match:
                                shieldings = line.split()
                                sf.write(shieldings[4])
                                sf.write('\n')
    def xyz_to_aev(self, xyz):
        '''
        XYZ to AEV using an inhouse c++ program. Need to find a better way to do this if it becomes popular
        '''
        command = "./xyz_to_aev" + " " + xyz + " >" + xyz[:-4] + ".aev" 
        subprocess.call(command, shell=True)

    def gen_temp_atom_aev(self):
        '''
        '''
        for filename in sorted(os.listdir(self.working_directory)):
            if filename.endswith('.aev'):
                temp_file = filename[:-4] + ".temp"

                aev = np.genfromtxt(filename)

                for atom_aev in aev:
                    str(atom_aev[0]) == self.atom_type


    def log_to_xyz(self):
        
        for filename in sorted(os.listdir(self.working_directory)):
            if filename.endswith('.log'):
                xyz_file = filename[:-4] + ".xyz"

                # Get Number of Atoms
                natoms_pattern = re.compile('NAtoms=')
                coords_pattern = re.compile('Input orientation:')

                with open(filename, 'r') as f:
                    for line in f:
                        match = re.search(natoms_pattern, line)
                        if match:
                           temp = line.split()
                           natoms = temp[1]
                           # print(natoms)

                # Print XYZ Coords
                with open(filename, 'r') as f:
                    for line in f:
                        match = re.search(coords_pattern, line)
                        if match:
                            coords = line[i + natoms].strip()
                            print(coords)


                    









    def run(self):
        #print('get_shieldings()')
        #print('consruct_aev()')
        #print('parse_aev_based on atom type')
        #print('run_shielding_correction()')

        return "Finished"
         




        
if __name__ == "__main__":

    predict_shieldings = ensemble_net(atom = 'C', directory=os.getcwd())
    predict_shieldings.xyz_to_aev('methane.xyz')

