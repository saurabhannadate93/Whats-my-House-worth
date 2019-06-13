"""
This module contains functions to train the model

"""
import os
import logging
import boto3
import yaml
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import datetime

logger = logging.getLogger()

def train_model_local(config):
    """Loads the input data and trains the model
    
    The trained model is saved in models/<model-name>

    Args:  
        config: config dictionary
 
    Returns: None
    """
    logger.debug('Running the train_model_local function')
    #Loading the file
    logger.debug("Loading the raw file.")
    try:
        data = pd.read_csv(os.path.join(config["generate_features"]["save_location"],config["generate_features"]["output_file_name"]))
    except Exception as e:
        logger.error(e)
        return

    #Training model
    logger.debug('Successfully loaded the input file. Training the model now.')
    try:
        data_filtered = data[config["train_model"]["fields"]]
        data_filtered = pd.get_dummies(data_filtered)
        features = np.array(data_filtered)
        labels = np.array(data[config["train_model"]["response"]])
        model_setup = RandomForestRegressor(**config['train_model']['params'])
        model = model_setup.fit(features,labels)
        
    except Exception as e:
        logger.error(e)
        return

    #Writing the model
    logger.debug('Successfully trained the model. Writing the model.')
    try:
        model_name = config['train_model']['model'] + "_" + config['train_model']['version'] + ".pkl"
        model_eval_name = config['train_model']['model'] + "_" + config['train_model']['version'] + ".txt"
        pickle.dump(model, open(os.path.join(config['train_model']['save_location'], model_name),'wb'))

        logger.debug('Model Written. Writing model performance metric')
        f = open(os.path.join(config['train_model']['save_location'], model_eval_name),"w+")
        f.write('Performance measures for model: {}\n'.format(model_name))
        f.write('Date of run: {} \n'.format(str(datetime.datetime.now())))
        f.write('OOB R-square: %0.3f\n' % model.oob_score_)
        f.close()
        logger.info('Model has been successfully trained and the model and the performance metric has been written in {}'.format(config['train_model']['save_location']))

    except Exception as e:
        logger.error(e)
        return

def train_model_AWS(config, bucket_name):
    """Loads the input data and trains the model
    
    The trained model is saved in <s3-bucket-name>/models/<model-name>

    Args:  
        config: config dictionary
 
    Returns: None
    """
    logger.debug('Running the train_model_AWS function')
    #Loading the file
    logger.debug("Loading the raw file.")
    try:    
        client = boto3.client('s3')
        resource = boto3.resource('s3')
        obj = client.get_object(Bucket=bucket_name, Key=config['generate_features']['save_location'] + "/" + config['generate_features']['output_file_name'])
        my_bucket = resource.Bucket(bucket_name)
        data = pd.read_csv(obj['Body'])

    except Exception as e:
        logger.error(e)
        return

    #Training model
    logger.debug('Successfully loaded the input file. Training the model now.')
    try:
        data_filtered = data[config["train_model"]["fields"]]
        data_filtered = pd.get_dummies(data_filtered)
        features = np.array(data_filtered)
        labels = np.array(data[config["train_model"]["response"]])
        model_setup = RandomForestRegressor(**config['train_model']['params'])
        model = model_setup.fit(features,labels)
        
    except Exception as e:
        logger.error(e)
        return

    #Writing the model
    logger.debug('Successfully trained the model. Writing the model.')
    try:
        model_name = config['train_model']['model'] + "_" + config['train_model']['version'] + ".pkl"
        model_eval_name = config['train_model']['model'] + "_" + config['train_model']['version'] + ".txt"
        pickle.dump(model, open(os.path.join(config['train_model']['save_location'], model_name),'wb'))

        f = open(os.path.join(config['train_model']['save_location'], model_eval_name),"w+")
        f.write('Performance measures for model: {}\n'.format(model_name))
        f.write('Date of run: {} \n'.format(str(datetime.datetime.now())))
        f.write('OOB R-square: %0.3f\n' % model.oob_score_)
        f.close()

        my_bucket.upload_file(os.path.join(config['train_model']['save_location'], model_name),Key=config['train_model']['save_location'] + "/" + model_name)
        os.remove(os.path.join(config['train_model']['save_location'], model_name))

        logger.debug('Model Written. Writing model performance metric')

        my_bucket.upload_file(os.path.join(config['train_model']['save_location'], model_eval_name),Key=config['train_model']['save_location'] + "/" + model_eval_name)
        os.remove(os.path.join(config['train_model']['save_location'], model_eval_name))
        logger.info('Model has been successfully trained and the model and the performance metric has been written in {}'.format(bucket_name + "/" + config['train_model']['save_location']))
    
    except Exception as e:
        logger.error(e)
        return

def train_model(args):
    '''Trains the model based on the configurations provided
    
    Args:
        args: Argparse args - includes args.where
        
    Returns:
        None
    '''
    logger.debug('Running the train_model function')

    with open(os.path.join("config","config.yml"), "r") as f:
        config = yaml.safe_load(f)

    if args.where == "Local":
        train_model_local(config)

    elif args.where == "AWS":
        train_model_AWS(config, args.bucket)
            
    else:
        logger.error('Kindly check the arguments and rerun. To understand different arguments, run `python run.py --help`')
        return