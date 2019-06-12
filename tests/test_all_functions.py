"""
This module contains functions to unit test all functions

"""
import pandas as pd
import numpy as np
import sys
import os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../src/')

from helpers.helpers import impute_by_NA, impute_by_zero, missing_check
from features import add_features

test_case11 = pd.DataFrame({'col1': ['a', 'b', None, 'c'], 'col2': ['x', None, None, None]})
check11 = pd.DataFrame({'col1': ['a', 'b', "Not_Available", 'c'], 'col2': ['x', "Not_Available", "Not_Available", "Not_Available"]})

def test_impute_by_NA1():
    assert (impute_by_NA(test_case11, ['col1', 'col2']) != check11).sum().sum() == 0



test_case21 = pd.DataFrame({'col1': [1, None, None, 'checking'], 'col2': [50, None, None, 'Hello']})
check21 = pd.DataFrame({'col1': [1, 0, 0, 'checking'], 'col2': [50, 0, 0, 'Hello']})

def test_impute_by_zero1():
    assert (impute_by_zero(test_case21, ['col1', 'col2']) != check21).sum().sum() == 0


test_case31 = pd.DataFrame({'col1': [1, 2, 3, 4], 'col2': [50, None, None, 'Hello'], 'col3': [25, None, "abcd", 1234], 'col4': ["That's", "What", "She", "Said"]})
check31 = [False, ['col2','col3']]

def test_missing_check1():
    assert missing_check(test_case31) == check31


test_case41 = pd.DataFrame({'YearBuilt': [1945, 1880, 2000, 1950], 'YearRemodAdd': [1955, 1880, 2010, 1950]})
check41 = pd.DataFrame({'YearBuilt': [1945, 1880, 2000, 1950], 'YearRemodAdd': [1955, 1880, 2010, 1950], 'RemodelledFlag' : ['Yes', 'No', 'Yes', 'No']})

def test_add_features1():
    assert (add_features(test_case41) != check41).sum().sum() == 0
