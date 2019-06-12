import logging
 
logger = logging.getLogger()


import datetime
import yaml
import os

import sqlalchemy
from sqlalchemy.orm import sessionmaker

def impute_by_zero(df, cols):
    """Imputes the missing values in the list of fields by 0 in the given dataframe
    """
    for i in cols:
        df[i].fillna(0,inplace=True)

    return df
def impute_by_NA(df, cols):
    """Imputes the missing values in the list of fields by "Not_Available" in the given dataframe
    """
    for i in cols:
        df[i].fillna("Not_Available",inplace=True)
    return df

def missing_check(df):
    """Imputes the missing values in the list of fields specified by "Not_Available"

    Args:
        df: Dataframe to be checked
    
    Returns:
        [True]: If the dataframe has no missing, a list is returned with 
        [False, missing_list]: If the dataframe has missing values, a list is returned with the first element as False and the second element as the list of fields with missing data
    """
    missing_list = []
    for i in df.columns:
        if df[i].isnull().sum().sum() != 0:
            missing_list.append(i)
    if len(missing_list) > 0:
        return [False, missing_list]
    else:
        return [True]


def format_sql(sql, replace_sqlvar=None, replace_var=None, python=True):
    """Formats SQL query string for Python interpretation and with variables replaced.

    Args:
        sql (string): String with SQL query
        replace_sqlvar (dict, optional): If given, replaces variables of the format ${var:dict-key} with the value
            in the dictionary corresponding to that dict-key.
        replace_var (dict, optional): If given, replaces variables of the format {dict-key} with the value
            in the dictionary corresponding to that dict-key.
        python: If True, formats the query to be passed into a Python SQL querying function by replacing "%" with
            "%%" since % is a special character in Python

    Returns: string of SQL query with variables replaced and optionally formatted for Python

    """
    if replace_sqlvar is not None:
        for var in replace_sqlvar:
            sql = sql.replace("${var:%s}" % var, replace_sqlvar[var])

    if replace_var is not None:
        sql = sql.format(**replace_var)

    if python:
        sql = sql.replace("%", "%%")

    return sql


def ifin(param, dictionary, alt=None):

    assert type(dictionary) == dict
    if param in dictionary:
        return dictionary[param]
    else:
        return alt


def create_connection(host='127.0.0.1', database="", sqltype="", port=10000,
                      user_env="", password_env="",
                      username=None, password=None, dbconfig=None, engine_string=None):

    if engine_string is None:
        if dbconfig is not None:
            with open(dbconfig, "r") as f:
                db = yaml.load(f)

            host = db["host"]
            database = ifin("dbname", db, "")
            sqltype = ifin("type", db, sqltype)
            port = db["port"]
            user_env = db["user_env"]
            password_env = db["password_env"]

        username = os.environ.get(user_env) if username is None else username
        password = os.environ.get(password_env) if password is None else password

        engine_string = "{sqltype}://{username}:{password}@{host}:{port}/{database}"
        engine_string = engine_string.format(sqltype=sqltype, username=username,
                                             password=password, host=host, port=port, database=database)

    conn = sqlalchemy.create_engine(engine_string)

    return conn


def get_session(engine=None, engine_string=None):
    """

    Args:
        engine_string: SQLAlchemy connection string in the form of:

            "{sqltype}://{username}:{password}@{host}:{port}/{database}"

    Returns:
        SQLAlchemy session
    """

    if engine is None and engine_string is None:
        return ValueError("`engine` or `engine_string` must be provided")
    elif engine is None:
        engine = create_connection(engine_string=engine_string)

    Session = sessionmaker(bind=engine)
    session = Session()

    return session
