"""
Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

To understand different arguments, run `python run.py --help`
"""
import os
import argparse
import config.config as config
import logging
import logging.config

# The logging configurations are called from local.conf
logging.config.fileConfig(os.path.join("config","logging_local.conf"))
logger = logging.getLogger(config.LOGGER_NAME)

from src.load_data import run_loading
from src.log_usage_data import create_db

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the run source code")
    subparsers = parser.add_subparsers()
    
    # Sub-parser for downloading the raw data
    sb_fetch = subparsers.add_parser("fetch", description="Fetch the raw data from the source")
    sb_fetch.add_argument("--where", default="Local", help="'Local' or 'AWS'; The destination bucket name needs to be provided in case of AWS")
    sb_fetch.add_argument("--bucket", default="None", help="Destination S3 bucket name")
    sb_fetch.set_defaults(func=run_loading)

    
    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database to track usage logs")
    sb_create.add_argument("--where", default="Local", help="'Local' or 'AWS'")
    sb_create.add_argument("--manual", default="no", help="Set as 'yes' if manually inputing RDS db credentials. Seeks variables from environment by default")
    sb_create.set_defaults(func=create_db)

    args = parser.parse_args()
    args.func(args)
