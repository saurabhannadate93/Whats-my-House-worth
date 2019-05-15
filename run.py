"""
Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

To understand different arguments, run `python run.py --help`
"""
import os
BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
 
import argparse
import logging.config
import config.logging_config as lconfig

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger

######TO BE RESOLVED

#logging.config.fileConfig(os.path.join(BASE_DIR, lconfig.REPO_NAME, "config", "logging", "logging.conf"))
logger = logging.getLogger("run-house-prices")

from src.load_data import run_loading
#from src.log_usage_data import create_db


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()
    
    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("fetch", description="Fetch the raw data from the source")
    sb_ingest.add_argument("--where", default="Local", help="'Local' or 'AWS'; bucket name needs to be provided in case of AWS")
    sb_ingest.add_argument("--bucket", default="None", help="S3 bucket name")
    sb_ingest.set_defaults(func=run_loading)

    
    # Sub-parser for creating a database
#    sb_create = subparsers.add_parser("create_db", description="Create database")
#    sb_ingest.add_argument("--where", default="Local", help="'Local' or 'AWS'; RDS host name needs to be provided in case of AWS")
#    sb_ingest.add_argument("--rds_host", default="None", help="RDS Host name")
#    sb_create.set_defaults(func=create_db)

    args = parser.parse_args()
    args.func(args)
