"""
Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

To understand different arguments, run `python run.py --help`
"""
import os
import argparse
import logging
import logging.config
import yaml

with open(os.path.join("config","config.yml"), "r") as f:
    config = yaml.safe_load(f)

# The logging configurations are called from local.conf
logging.config.fileConfig(os.path.join("config","logging_local.conf"))
logger = logging.getLogger(config['logging']['LOGGER_NAME'])

from src.load_data import load_data
from src.clean_data import clean_data
from src.generate_features import generate_features
from src.train_model import train_model
from src.log_usage_data import create_db
from app.app import run_app

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the run source code")
    subparsers = parser.add_subparsers()
    
    # Sub-parser for downloading the raw data
    sb_fetch = subparsers.add_parser("load_data", description="Fetch the raw data from the source")
    sb_fetch.add_argument("--where", default="Local", help="'Local' or 'AWS'; The destination bucket name needs to be provided in case of AWS")
    sb_fetch.add_argument("--bucket", default="None", help="Destination S3 bucket name")
    sb_fetch.set_defaults(func=load_data)

    
    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database to track usage logs")
    sb_create.add_argument("--where", default="Local", help="'Local' or 'AWS'")
    sb_create.add_argument("--manual", default="no", help="Set as 'yes' if manually inputing RDS db credentials. Seeks variables from environment by default")
    sb_create.set_defaults(func=create_db)


    # Sub-parser for cleaning the data
    sb_clean = subparsers.add_parser("clean_data", description="Clean the raw data")
    sb_clean.add_argument("--where", default="Local", help="'Local' or 'AWS'; The destination bucket name needs to be provided in case of AWS")
    sb_clean.add_argument("--bucket", default="None", help="Destination S3 bucket name")
    sb_clean.set_defaults(func=clean_data)

    # Sub-parser for generating the features
    sb_gen_features = subparsers.add_parser("generate_features", description="Clean the raw data")
    sb_gen_features.add_argument("--where", default="Local", help="'Local' or 'AWS'; The destination bucket name needs to be provided in case of AWS")
    sb_gen_features.add_argument("--bucket", default="None", help="Destination S3 bucket name")
    sb_gen_features.set_defaults(func=generate_features)


    # Sub-parser for training the model
    sb_train_model = subparsers.add_parser("train_model", description="Trains the model")
    sb_train_model.add_argument("--where", default="Local", help="'Local' or 'AWS'; The destination bucket name needs to be provided in case of AWS")
    sb_train_model.add_argument("--bucket", default="None", help="Destination S3 bucket name")
    sb_train_model.set_defaults(func=train_model)


    # Sub-parser for starting the app
    sb_run_app = subparsers.add_parser("run_app", description="Trains the model")
    sb_run_app.add_argument("--where", default="Local", help="'Local' or 'AWS'; The S3 bucket name needs to be provided in case of AWS")
    sb_run_app.add_argument("--bucket", default="None", help="S3 bucket name from where to source the model")
    sb_run_app.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)
