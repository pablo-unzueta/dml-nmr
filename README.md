# DML-NMR
Delta-Machine Learning Nuclear Magnetic Resonance (**DML-NMR**) is a set of python scripts to rapidly predict isotropic chemical shieldings at the PBE0/6-311+G(2d,p) level of theory. DML-NMR relies on calculating an inexpensive chemical shielding using *Gaussian09* (or newer) in combination with these python scripts.

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
### XYZ to AEV files

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
