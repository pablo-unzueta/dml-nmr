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
        self.model = self.load_weights()
        self.get_shieldings_from_log()

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

    def get_shieldings_from_log(self):

        search_term = self.atom_type + "    Isotropic"

        pattern = re.compile(search_term)

        for filename in sorted(os.listdir(self.working_directory)):
            if filename.endswith('.log'):
                shift_file = filename[:-4] + ".shifts"

                with open(filename, 'r') as f:
                    with open(shift_file, 'w') as sf:
                        for line in f:
                            match = re.search(pattern, line)
                            if match:
                                shieldings = line.split()
                                sf.write(shieldings[4])
                                sf.write('\n')
    def xyz_to_aev(self):
        '''
        XYZ to AEV using an inhouse c++ program. Need to find a better way to do this if it becomes popular
        '''
        command = "./xyz_to_aev" + " " + self.xyz + " >" + self.xyz[:-4] + ".aev" 
        subprocess.call(command, shell=True)

    def gen_temp_atom_aev(self):
        '''
        '''
        temp_aev = []
        for filename in sorted(os.listdir(self.working_directory)):
            if filename.endswith('.aev'):
                temp_file = filename[:-4] + ".temp"

                aev = np.genfromtxt(filename, delimiter=',')

                # Atom type Dictionary
                atom_dict = {'C' : 6.0,
                     'H' : 1.0,
                     'N' : 15.0,
                     'O' : 17.0}
               
                for vector in aev:
                    if(vector[0] == atom_dict[self.atom_type]):
                        #print(vector[1:385])
                        temp_aev.append(vector[1:385])

                #for atom_aev in aev:
                #    str(atom_aev[0]) == self.atom_type
                temp_aev = np.asarray(temp_aev)
                np.savetxt(temp_file, temp_aev)


    def log_to_xyz(self):
        
        for filename in sorted(os.listdir(self.working_directory)):
            if filename.endswith('.log'):
                xyz_file = filename[:-4] + ".xyz"
                self.xyz = xyz_file

                # Get Number of Atoms
                natoms_pattern = re.compile('NAtoms=')
                coords_pattern = re.compile('Input orientation:')

                with open(filename, 'r') as f:
                    for line in f:
                        match = re.search(natoms_pattern, line)
                        if match:
                           temp = line.split()
                           natoms = temp[1]
                           #print(natoms)

                # Print XYZ Coords
                with open(filename, 'r') as f:
                    lines = f.readlines()
                    for index, line in enumerate(lines):
                        match = re.search(coords_pattern, line)
                        if match:
                            with open(xyz_file, 'w') as xyz_f:
                                xyz_f.write(f"{natoms}\n")
                                xyz_block = lines[index+5:index+14]
                                for coord in xyz_block:
                                    coord = coord.split()
                                    xyz_f.write(f"{coord[1]}\t{coord[3]}\t{coord[4]}\t{coord[5]}\n")
                                    #print(f"{coord[1]}\t{coord[3]}\t{coord[4]}\t{coord[5]}")
                            #xyz_block = lines.split()
                            #print(xyz_block)
                            # print(f[index])

    def calc_dml_nmr(self):
        
        for filename in sorted(os.listdir(self.working_directory)):
            if filename.endswith('.temp'):
                #print(filename)
                dml_file = filename[:-5] + ".dml"
                cheap_shielding_file = filename[:-5] + ".shifts"

                self.cheap_shieldings = np.genfromtxt(cheap_shielding_file)
                data = np.genfromtxt(filename)

                # Need next line in case there is only 1 atom
                # to avoid 0-D data
                data = data.reshape((-1,384))
            
                ensemble_ml_corrs = self.model.predict(data)
                ensemble_ml_corrs = np.asarray(ensemble_ml_corrs) 
        
                delta_correct = ensemble_ml_corrs[0]
                ml_corrs = ensemble_ml_corrs[1]
                
                #print(delta_correct)
                print(delta_correct)
                        
                dml_shifts = self.cheap_shieldings + delta_correct[:,0]
        
                
                np.savetxt(dml_file, dml_shifts, fmt="%1.5f")
                
                if(self.std):
                    std_file = filename[:-5] + ".std"
                    std_corrs = np.std(ml_corrs, axis=0)

                    #print(std_corrs)
                    np.savetxt(std_file, std_corrs, fmt="%1.5f")



#    def clean_up(self):


    def print_end_call(self):

        print('\n\n\n')
        print('******************************************************')
        print('\tDML-NMR Complete! Buy Pablo Coffee')
        print('******************************************************')
        print("""              
                               (
                                )     (
                         ___...(-------)-....___
                     .-""       )    (          ""-.
               .-'``'|-._             )         _.-|
              /  .--.|   `""---...........---""`   |
             /  /    |                             |
             |  |    |                             |
              \  \   |                             |
               `\ `\ |                             |
                 `\ `|                             |
                 _/ /\                             /
                (__/  \                           /
             _..---""` \                         /`""---.._
          .-'           \                       /          '-.
         :               `-.__             __.-'              :
         :                  ) ""---...---"" (                 :
          '._               `"--...___...--"`              _.'
            \""--..__                              __..--""/
             '._     ""-----.....______.....-----"     _.'
                `""--..,,_____            _____,,..--""`
                              `""------"`
        """)

        


    def run(self):
        self.log_to_xyz()
        self.xyz_to_aev()
        self.gen_temp_atom_aev()
        self.calc_dml_nmr()
        self.print_end_call()
        #print('get_shieldings()')
        #print('consruct_aev()')
        #print('parse_aev_based on atom type')
        #print('run_shielding_correction()')

        return "Finished"
         
if __name__ == "__main__":

    predict_shieldings = ensemble_net(atom = 'C', directory=os.getcwd(), std=False)
    predict_shieldings.run()
    #predict_shieldings.log_to_xyz()
    #predict_shieldings.get_shieldings_from_log()
    #predict_shieldings.xyz_to_aev('methane.xyz')
    #predict_shieldings.calc_dml_nmr()
        #predict_shieldings.gen_temp_atom_aev()
    #predict_shieldings.print_end_call()

