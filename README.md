# DML-NMR
Delta-Machine Learning Nuclear Magnetic Resonance (**DML-NMR**) is a set of python scripts to rapidly predict isotropic chemical shieldings at the PBE0/6-311+G(2d,p) level of theory. DML-NMR relies on calculating an inexpensive chemical shielding using *Gaussian09* (or newer) in combination with these python scripts.

![NN Ensemble Net](https://github.com/pablo-unzueta/dml-nmr/blob/main/images/nn_arch_and_ensemble_combined_large_font_cropped.svg)


This project was developed by Pablo Unzueta and Gregory Beran at UC Riverside. Visit our [group website](https://research.chem.ucr.edu/groups/beran/publications.html) for our full publication list.

# Installation

## Dependencies
* Tensorflow (>= 2.0)
* Numpy (>= 1.13.3)
* Scikit-Learn (>= 0.23.2)
* Pandas (>= 1.1.3)
* GCC (>= 9.3.0)

DML-NMR python scripts are written for **python3.7** or newer.
## User Installation
The preferred method of installation is through `pip`:

    pip install -U dml-nmr

or `conda`

    conda install -c conda-forge dml-nmr

## Source Code
Source code can be viewed with the following command:

    git clone https://github.com/pablo-unzueta/dml-nmr

# Usage

## Examples
Using **DML-NMR** is quite simple. The code simply acts on all *Gaussian09* output or `.log` files. For example, in a directory containing all the NMR *Gaussian09* `.log` files calculated at the PBE0/6-31G level of theory and basis set.

    from dmlnmr import ensemble_net
    import os 
    current_dir = os.getcwd()

    predict_shieldings = ensemble_net(atom='C')
    predict_shieldings(current_dir)

Will produce `.dml` files for each corresponding `.log` file containing the new PBE0/6-311+G(2d,p) shielding predictions for every carbon atom. Accepted atom types are `C` `H` `N` and `O`

If you have calculated chemical shieldings using a different density functional or basis set, you can change the `ensemble_net()` function call:

    predict_shieldings = ensemble_net(atom='C', dft='PBE', basis_set='STO-3G')

Currently, we have trained nets for following density functionals:
* `LDA`
* `PBE`
* `PBE0`

And basis sets:
* `STO-3G`
* `6-31G`

Lastly, the advantage of using an ensemble net allows one to examine the uncertainty of prediction between the individual members to assess the quality of the prediction. By using the following argument:

    predict_shieldings = ensemble_net(atom='C', std=True)

another set of files with the `.std` extension will be produced corresponding to the standard deviation of each new shielding precition. Please refer to our paper(add link to paper) to examine the 95% confidence intervals of each prediction.

If you have downloaded the source code from github, you can use the driver `predict_shieldings.py` which acts on a directory of *Gaussian09* output or `.log` files. Using the following command in the `examples/predict/` directory will produce `.dml` files for each `.log` file.

    python predict_shieldings.py

If you wish to examine the uncertainties of each prediction, you can use:

    python predict_shieldings.py --std=True 

which will produce another set files with the `.std` extension corresponding the standard deviation from the ensemble nets of each prediction.

### XYZ to AEV files
Included in the `examples/aev` directory is a c++ executable to calculate the elements of the atomic environment vector (AEV). This can be used as a standalone module to generate AEVs for simple `.xyz` files.

    methane.xyz ./xyz_to_aev > methane.aev

The `methane.aev` file is also included to quickly check if this working properly on your machine. Furthermore, the `./xyz_to_aev` is also called when using `predict_shieldings.py` for new NMR shielding predictions.

 


## Re-Training Neural Nets
Neural networks were trained using the methods detailed in the publication. If you'd like to re-train the neural networks, then follow these steps.
1. Download the pandas dataframe files hosted on [figshare](https://figshare.com/)
2. Place these files in the `train/data/` directory
3. Modify kfold_90_10.py training script with new training protocol
4. Run using `python kfold_90_10.py > results.out`

The new training weights are saved as `.h5` files. Move these files to the corresponding directory for your desired level of theory and basis set.


# Citation
Please cite if using this software:

    XXX-XXXX
