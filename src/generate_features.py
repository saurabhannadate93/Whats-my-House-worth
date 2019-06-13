"""
This module uses the functions in the features.py to add in more features to the dataset

"""
import os
import logging
import boto3
import yaml
import pandas as pd
from src.features import add_features

logger = logging.getLogger()


def generate_features_local(config):
    '''Generates the features defined in the add_features method in the dataframe provided
    
    All cleaned data is dumped at /data/features

    Args:
        config: Config dictionary
        
    Returns:
        None
    '''
    logger.debug('Running the generate_features_local function')

    #Loading the raw input file
    logger.debug("Loading the raw file.")
    try:
        cleaned_data = pd.read_csv(os.path.join(config['clean_data']['save_location'], config['clean_data']['output_file_name']))

    except FileNotFoundError:
        logger.error("FileNotFound: Please check whether the cleaned data file exists, or the file name is accurate in the config file and retry.")
        return
    
    except Exception as e:
        logger.error(e)
        return

    #Generate features
    logger.debug("Cleaned file successfully loaded. Starting feature generation process.")
    try:
        data_with_features = add_features(cleaned_data)
    except Exception as e:
        logger.error(e)
        return

    logger.debug("Features generated. Writing file now.")
    try:
        data_with_features.to_csv(os.path.join(config['generate_features']['save_location'], config['generate_features']['output_file_name']))
    except Exception as e:
        logger.error(e)
        return
    else:
        logger.info('Features have been generated and the dataset has been saved at {}'.format(config['generate_features']['save_location']))
        return

def generate_features_AWS(config, bucket_name):
    '''Generates the features defined in the add_features method in the dataframe provided
    
    All cleaned data is dumped at <s3-bucket name>/data/features
    
    Args:
        config: Config dictionary
        bucket_name: target bucket name used for all analysis
        
    Returns:
        None
    '''
    logger.debug('Running the generate_features_AWS function')

    #Loading the raw input file
    logger.debug("Loading the raw file.")
    try:    
        client = boto3.client('s3')
        resource = boto3.resource('s3')
        obj = client.get_object(Bucket=bucket_name, Key=config['clean_data']['save_location'] + "/" + config['clean_data']['output_file_name'])
        my_bucket = resource.Bucket(bucket_name)
        cleaned_data = pd.read_csv(obj['Body'])

    except Exception as e:
        logger.error(e)
        return

    #Generate features
    logger.debug("Cleaned file successfully loaded. Starting feature generation process.")
    try:
        data_with_features = add_features(cleaned_data)
    except Exception as e:
        logger.error(e)
        return

    logger.debug("Features generated. Writing file now.")
    try:
        data_with_features.to_csv(os.path.join(config['generate_features']['save_location'], config['generate_features']['output_file_name']))
        my_bucket.upload_file(os.path.join(config['generate_features']['save_location'], config['generate_features']['output_file_name']),Key=config['generate_features']['save_location'] + "/" + config['generate_features']['output_file_name'])
        os.remove(os.path.join(config['generate_features']['save_location'], config['generate_features']['output_file_name']))
    except Exception as e:
        logger.error(e)
        return
    else:
        logger.info('Features have been generated and the dataset has been saved at {}'.format(bucket_name + "/" +config['generate_features']['save_location']))
        return

        
def generate_features(args):
    '''Generates the features required for modeling
    
    Args:
        args: Argparse args - includes args.where, args.bucket 
            args.where: 'Local' or 'AWS'
            args.bucket (required if args.where = 'AWS'): S3 bucket for all analysis
        
    Returns:
        None
    '''
    logger.debug('Running the generate_features function')

    with open(os.path.join("config","config.yml"), "r") as f:
        config = yaml.safe_load(f)

    if args.where == "Local":
        generate_features_local(config)

    elif args.where == "AWS":
        generate_features_AWS(config, args.bucket)
            
    else:
        logger.error('Kindly check the arguments and rerun. To understand different arguments, run `python run.py --help`')
        return