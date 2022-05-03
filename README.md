# DML-NMR
Delta-Machine Learning Nuclear Magnetic Resonance (**DML-NMR**) is a set of python scripts to rapidly predict isotropic chemical shieldings at the PBE0/6-311+G(2d,p) level of theory. DML-NMR relies on calculating an inexpensive chemical shielding using *Gaussian09* (or newer) in combination with these python scripts.

<p align="center">
  <img src="https://github.com/pablo-unzueta/dml-nmr/blob/main/images/nn_arch_and_ensemble_combined_large_font_cropped.svg">
</p>

This project was developed by Pablo Unzueta and Gregory Beran at UC Riverside. Visit our [group website](https://beran.chem.ucr.edu/publications.html) for our full publication list.

# Installation

## Dependencies
* tensorflow >= 2.0
* numpy >= 1.13.3
* Sklearn >= 0.23.2
* pandas >= 1.1.3
* torchani >= 2.2

DML-NMR python scripts are written for **python3.7** or newer.
## User Installation
Source code can be downloaded with the following command:

    git clone https://github.com/pablo-unzueta/dml-nmr

# Usage

## Examples
Using **DML-NMR** is quite simple. The code simply acts on all *Gaussian09* output (`.log`) files in a directory. All options are controlled in the example **config.yml** file. Once all options are set, simply type:

    python main.py

This will produce `.dml` files for each corresponding `.log` file containing the new PBE0/6-311+G(2d,p) shielding predictions in the first column, and the standard deviation of the ensemble predictions in the second column. Please note that the only accepted atom types are `C` `H` `N` and `O`.
The advantage of using an ensemble net allows one to examine the uncertainty between the individual members to assess the quality of the prediction. Please refer to our [paper](https://pubs.acs.org/doi/abs/10.1021/acs.jctc.0c00979) to examine the 95% confidence intervals per atom type.


Currently, we have trained nets for following density functionals:
* `LDA`
* `PBE`
* `PBE0`

And basis sets:
* `STO-3G`
* `6-31G`

We suggest using *PBE0/6-31G* for the baseline calculation and have included the ensemble uncertainties below for this model per atom type. If the NMR calculations become a significant bottleneck, one can opt of the cheaper *PBE/6-31G* calculations which are roughly 30% cheaper as discussed in the paper.

 

### Carbon Shielding Error 95% Confidence Interval 
| Stdev | PBE0/6-31G (ppm) | PBE/6-31G (ppm) |
| :------------- | :-------------: | :-------------: |
| < 0.25 | 1.0 | 1.0|
| 0.25 - 0.5 | 1.4 | 1.5 |
| 0.5 - 0.75 | 1.9 | 2.3 |
| 0.75 - 1.0 | 2.5 | 2.8 |
| > 1.0 | 3.2 | 4.0 |


### XYZ to AEV Conversion
The xyz to aev file conversion is carried out using the [torchani](https://github.com/aiqm/torchani) python package. It is highly recommended to only carry out this process once since generating AEV's can be time consuming for a large quantity of files. 
Once the code has been ran once, please modify **config.yml** to the following: 

    reprocess_aev: False

# Citation
Please cite if using this software:

```

@ARTICLE{Unzueta2021-rx,
  title    = "Predicting Density Functional {Theory-Quality} Nuclear Magnetic
              Resonance Chemical Shifts via {$\Delta$-Machine} Learning",
  author   = "Unzueta, Pablo A and Greenwell, Chandler S and Beran, Gregory J O",
  journal  = "J. Chem. Theory Comput.",
  volume   =  17,
  number   =  2,
  pages    = "826--840",
  month    =  feb,
  year     =  2021,
  language = "en",
  issn     = "1549-9618, 1549-9626",
  doi      = "10.1021/acs.jctc.0c00979"
}

```
