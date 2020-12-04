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

class ensemble_net:
    def __init__(self, atom, dft='PBE0', basis_set='6-31G', std=False):
        self.atom_type = atom
        self.dft = dft
        self.basis_set = basis_set
        self.std = std
        

