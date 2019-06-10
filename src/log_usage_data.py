import os
import logging
import logging.config
import datetime

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

import yaml
import argparse

import getpass
import pymysql

logger = logging.getLogger()

Base = declarative_base()

class usage_log(Base):
    """ Defines the data model for the table `usage_log`. """

    __tablename__ = 'usage_log'
    
    Usage_id = Column(Integer, primary_key=True, autoincrement=True, nullable = False)
    timestamp = Column(String(100), unique=False, nullable=False)
    LotArea = Column(Integer, unique=False, nullable=False)
    YearBuilt = Column(Integer, unique=False, nullable=False)
    TotalBsmtSF = Column(Integer, unique=False, nullable=False)
    FirstFlrSF = Column(Integer, unique=False, nullable=False)
    GrLivArea = Column(Integer, unique=False, nullable=False)
    FullBath = Column(Integer, unique=False, nullable=False)
    TotRmsAbvGrd = Column(Integer, unique=False, nullable=False)
    FirePlaces = Column(Integer, unique=False, nullable=False)
    GarageCars = Column(Integer, unique=False, nullable=False)
    GarageArea = Column(Integer, unique=False, nullable=False)
    PredictedPrice = Column(Float, unique=False, nullable=False)

    def __repr__(self):
        tweet_repr = "<UsageLog=(Usage_id='%s PredictedPrice='%d>"
        return tweet_repr % (self.Usage_id, self.PredictedPrice)


def create_db(args):
    """Creates a database with the data models inherited from `Base` (Usage_Log).

    Args:
        args: Argparse args - include args args.where and args.manual.

    Returns:
        None
    """
    with open(os.path.join("config","config.yml"), "r") as f:
        config = yaml.safe_load(f)

    logger.debug('Running the create_db function')
    
    if args.where == "Local":
        try:
            logger.info('Creating a local database at {}'.format(config['db_config']['SQLALCHEMY_DATABASE_URI']))
            engine = create_engine(config['db_config']['SQLALCHEMY_DATABASE_URI'])
            logger.debug('Database engine successfully created.')            
        except Exception as e:
            logger.error(e)
            
    elif args.where == "AWS":
        try:
            
            logger.info('Creating an RDS database based on environment variables: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB.')
            conn_type = "mysql+pymysql"
            user = os.environ.get("MYSQL_USER")
            password = os.environ.get("MYSQL_PASSWORD")
            host = os.environ.get("MYSQL_HOST")
            port = os.environ.get("MYSQL_PORT")
            db_name = os.environ.get("MYSQL_DB")
            engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, db_name)
        
            logger.debug('Creating database now.')    
            engine = create_engine(engine_string)            
            logger.debug('Database engine successfully created.')
        
        except Exception as e:
            logger.error("Database engine cannot be created. Kindly check the configurations and try again.")
            logger.error(e)
    
    else:
        raise ValueError('Kindly check the arguments and rerun. To understand different arguments, run `python run.py --help`')
    
    if args.where in ["AWS", "Local"]:    
        try:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            logger.info('Database successfully created.')            
    
        except Exception as e:
            logger.error("Database could not be created. Kindly check the configurations and try again.")
            logger.error(e)