"""
This module contains the function to create features

NOTE: Add to the add_features method as more features need to be developed and added
"""

import logging
import pandas as pd

logger = logging.getLogger()

def add_features(df):
    """Function to add additional functions to the data
    """
    try:
        df['RemodelledFlag'] = 'No'
        df.loc[(df['YearBuilt'] < df['YearRemodAdd']) ,'RemodelledFlag'] = 'Yes'
    
    except:
        raise
    
    else:
        return df
