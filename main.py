import os
import sys
import argparse
import yaml
from src import process
from src import models


def main():
    parser = argparse.ArgumentParser(description="DML-NMR inputs")
    parser.add_argument(
        "--config_path",
        default="config.yml",
        type=str,
        help="Location of config file (default: config.yml)",
    )
    parser.add_argument(
        "--model_path",
        default=None,
        type=str,
        help="path of the model files",
    )
    parser.add_argument(
        "--data_path",
        default=None,
        type=str,
        help="Location of data containing structures (json or any other valid format) and accompanying files",
    )
    parser.add_argument(
        "--dft",
        default=None,
        type=str,
        help="aev, lda, pbe, or pbe0",
    )
    parser.add_argument(
        "--basis",
        default=None,
        type=str,
        help="631g or sto3g",
    )
    parser.add_argument(
        "--reprocess_aev",
        default=None,
        type=bool,
        help="Generate AEV files. Can be time consuming if handling large amounts of data",
    )
    parser.add_argument(
        "--reprocess_shieldings",
        default=None,
        type=bool,
        help="Generate shieldings from gaussian .log files",
    )

    # Get arguments from command line
    args = parser.parse_args(sys.argv[1:])

    # Open provided config file
    assert os.path.exists(args.config_path), (
        "Config file not found in " + args.config_path
    )
    with open(args.config_path, "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    if args.data_path is not None:
        config["Processing"]["data_path"] = args.data_path
    if args.dft is not None:
        config["Processing"]["dft"] = args.atom_type
    if args.basis is not None:
        config["Processing"]["basis"] = args.atom_type
    if args.reprocess_aev is not None:
        config["Processing"]["reprocess_aev"] = args.reprocess_aev
    if args.reprocess_shieldings is not None:
        config["Processing"]["reprocess_shieldings"] = args.shieldings

    if config["Processing"]["dft"] == "aev":
        model_path = os.path.join("src/saved_nets", config["Processing"]["dft"])
    else:
        model_path = os.path.join("src/saved_nets",
                                  config["Processing"]["dft"] + "_" +
                                  config["Processing"]["basis"])

    config["Processing"]["model_path"] = model_path

    print("------------------------------------------------")
    print(f'Processing data from {config["Processing"]["data_path"]}')
    print("------------------------------------------------")

    process.process_data(config)

    print("------------------------------------------------")
    print(f'Loading model weights from {config["Processing"]["model_path"]}')
    print("------------------------------------------------")

    model = models.EnsembleNet(config)
    model.calc_dml_nmr(config)


if __name__ == "__main__":
    main()
