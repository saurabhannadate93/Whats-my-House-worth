"""
This module contains functions to clean the raw data
"""
import os
import logging
import boto3
import yaml
import pandas as pd

logger = logging.getLogger()

from src.helpers.helpers import impute_by_zero, impute_by_NA, missing_check


def run_cleaning_local(config):
    '''Cleans the raw training data and creates a new output
    
    All cleaned data is dumped at /data/clean

    Args:
        config: Config dictionary
        
    Returns:
        None
    '''
    logger.debug('Running the run_cleaning_local function')

    #Loading the raw input file
    logger.debug("Loading the raw file.")
    try:
        raw_data = pd.read_csv(os.path.join(config['load_data']['save_location'], config['clean_data']['input_file_name']))

    except FileNotFoundError:
        logger.error("FileNotFound: Please check whether the input data file exists, or the file name is accurate in the config file and retry.")
        return

    except Exception as e:
        logger.error(e)
        return

    #Cleaning the data
    logger.debug("Raw file successfully loaded. Starting cleaning process.")
    try:
        raw_data = impute_by_zero(raw_data, config['clean_data']['impute_by_zero'])
        raw_data = impute_by_NA(raw_data, config['clean_data']['impute_by_NA'])    
        raw_data.drop(config['clean_data']['delete_fields'], axis = 1, inplace = True) 

    except Exception as e:
        logger.error(e)
        return

    #Checking for missing values
    logger.debug("Checking for missing values.")
    if missing_check(raw_data)[0] == False:
        logger.error('Missing values in fields:{}'.format(missing_check(raw_data)[1]))
        logger.error('Please either impute or drop the fields. The config provides functionality to add the fields to be either imputed by 0 or by "Not_Available"')
        return

    logger.debug("Data cleaned. Writing cleaned file now.")
    try:
        raw_data.to_csv(os.path.join(config['clean_data']['save_location'], config['clean_data']['output_file_name']))
    except Exception as e:
        logger.error(e)
        return
    else:
        logger.info('Data has been cleaned and cleaned dataset has been saved at {}'.format(config['clean_data']['save_location']))
        return

def run_cleaning_AWS(config, bucket_name):
    '''Cleans the raw training data and creates a new output
    
    All cleaned data is dumped at <s3-bucket name>/data/clean
    
    Args:
        config: Config dictionary
        bucket_name: target bucket name used for all analysis
        
    Returns:
        None
    '''
    logger.debug('Running the run_cleaning_AWS function')

    #Loading the raw input file
    logger.debug("Loading the raw file.")
    try:    
        client = boto3.client('s3')
        resource = boto3.resource('s3')
        obj = client.get_object(Bucket=bucket_name, Key=config['load_data']['save_location'] + "/" + config['clean_data']['input_file_name'])
        my_bucket = resource.Bucket(bucket_name)
        raw_data = pd.read_csv(obj['Body'])

    except Exception as e:
        logger.error(e)
        return

    #Cleaning the data
    logger.debug("Raw file successfully loaded. Starting cleaning process.")
    try:
        raw_data = impute_by_zero(raw_data, config['clean_data']['impute_by_zero'])
        raw_data = impute_by_NA(raw_data, config['clean_data']['impute_by_NA'])    
        raw_data.drop(config['clean_data']['delete_fields'], axis = 1, inplace = True) 

    except Exception as e:
        logger.error(e)
        return

    #Checking for missing values
    logger.debug("Checking for missing values.")
    if missing_check(raw_data)[0] == False:
        logger.error('Missing values in fields:{}'.format(missing_check(raw_data)[1]))
        logger.error('Please either impute or drop the fields. The config provides functionality to add the fields to be either imputed by 0 or by "Not_Available"')
        return

    logger.debug("Data cleaned. Writing cleaned file now.")
    try:
        raw_data.to_csv(os.path.join(config['clean_data']['save_location'], config['clean_data']['output_file_name']))
        my_bucket.upload_file(os.path.join(config['clean_data']['save_location'], config['clean_data']['output_file_name']),Key=config['clean_data']['save_location'] + "/" + config['clean_data']['output_file_name'])
        os.remove(os.path.join(config['clean_data']['save_location'], config['clean_data']['output_file_name']))
    except Exception as e:
        logger.error(e)
        return
    else:
        logger.info('Data has been cleaned and cleaned dataset has been saved at {}'.format(bucket_name + "/" +config['clean_data']['save_location']))
        return

        
def clean_data(args):
    '''Fetches the data from the raw folder and cleans it
    
    Args:
        args: Argparse args - includes args.where
        
    Returns:
        None
    '''
    logger.debug('Running the clean_data function')

    with open(os.path.join("config","config.yml"), "r") as f:
        config = yaml.safe_load(f)

    if args.where == "Local":
        run_cleaning_local(config)

    elif args.where == "AWS":
        run_cleaning_AWS(config, args.bucket)
            
    else:
        logger.error('Kindly check the arguments and rerun. To understand different arguments, run `python run.py --help`')
        return