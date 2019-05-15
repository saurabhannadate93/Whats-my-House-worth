import os
import logging
import logging.config
import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

import config.config as config
import argparse

import getpass
import pymysql

logger = logging.getLogger(__name__)

Base = declarative_base()

class usage_log(Base):
    """ Defines the data model for the table `usage_log`. """

    __tablename__ = 'usage_log'
    
    Usage_id = Column(Integer, primary_key=True, autoincrement=True, nullable = False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow(), unique=False, nullable=False)
    MSSubClass = Column(String(100), unique=False, nullable=False)
    MSZoning = Column(String(100), unique=False, nullable=False)
    LotFrontage = Column(Integer, unique=False, nullable=False)
    LotArea = Column(Integer, unique=False, nullable=False)
    Street = Column(String(20), unique=False, nullable=False)
    Alley = Column(String(20), unique=False, nullable=False)
    LotShape = Column(String(100), unique=False, nullable=False)
    LandContour = Column(String(100), unique=False, nullable=False)
    Utilities = Column(String(100), unique=False, nullable=False)
    LotConfig = Column(String(100), unique=False, nullable=False)
    LandSlope = Column(String(100), unique=False, nullable=False)
    BldgType = Column(String(100), unique=False, nullable=False)
    HouseStyle = Column(String(100), unique=False, nullable=False)
    OverallQual = Column(Integer, unique=False, nullable=False)
    OverallCond = Column(Integer, unique=False, nullable=False)
    YearBuilt = Column(String(100), unique=False, nullable=False)
    YearRemodAdd = Column(String(100), unique=False, nullable=False)
    RoofStyle = Column(String(100), unique=False, nullable=False)
    RoofMatl = Column(String(100), unique=False, nullable=False)
    Exterior1st = Column(String(100), unique=False, nullable=False)
    Exterior2nd = Column(String(100), unique=False, nullable=False)
    MasVnrType = Column(String(100), unique=False, nullable=False)
    MasVnrArea = Column(Integer, unique=False, nullable=False)
    ExterQual = Column(String(100), unique=False, nullable=False)
    ExterCond = Column(String(100), unique=False, nullable=False)
    Foundation = Column(String(100), unique=False, nullable=False)
    BsmtQual = Column(String(100), unique=False, nullable=False)
    BsmtCond = Column(String(100), unique=False, nullable=False)
    BsmtExposure = Column(String(100), unique=False, nullable=False)
    BsmtFinType1 = Column(String(100), unique=False, nullable=False)
    BsmtFinSF1 = Column(Integer, unique=False, nullable=False)
    BsmtFinType2 = Column(String(100), unique=False, nullable=False)
    BsmtFinSF2 = Column(Integer, unique=False, nullable=False)
    BsmtUnfSF = Column(Integer, unique=False, nullable=False)
    TotalBsmtSF = Column(Integer, unique=False, nullable=False)
    Heating = Column(String(100), unique=False, nullable=False)
    HeatingQC = Column(String(100), unique=False, nullable=False)
    CentralAir = Column(String(100), unique=False, nullable=False)
    Electrical = Column(String(100), unique=False, nullable=False)
    FirstFlrSF = Column(Integer, unique=False, nullable=False)
    SecondFlrSF = Column(Integer, unique=False, nullable=False)
    LowQualFinSF = Column(Integer, unique=False, nullable=False)
    GrLivArea = Column(Integer, unique=False, nullable=False)
    BsmtFullBath = Column(Integer, unique=False, nullable=False)
    BsmtHalfBath = Column(Integer, unique=False, nullable=False)
    FullBath = Column(Integer, unique=False, nullable=False)
    HalfBath = Column(Integer, unique=False, nullable=False)
    BedroomAbvGr = Column(Integer, unique=False, nullable=False)
    KitchenAbvGr = Column(Integer, unique=False, nullable=False)
    KitchenQual = Column(String(100), unique=False, nullable=False)
    TotRmsAbvGrd = Column(Integer, unique=False, nullable=False)
    Functional = Column(String(100), unique=False, nullable=False)
    Fireplaces = Column(Integer, unique=False, nullable=False)
    FireplaceQu = Column(String(100), unique=False, nullable=False)
    GarageType = Column(String(100), unique=False, nullable=False)
    GarageYrBlt = Column(String(100), unique=False, nullable=False)
    GarageFinish = Column(String(100), unique=False, nullable=False)
    GarageCars = Column(Integer, unique=False, nullable=False)
    GarageArea = Column(Integer, unique=False, nullable=False)
    GarageQual = Column(String(100), unique=False, nullable=False)
    GarageCond = Column(String(100), unique=False, nullable=False)
    PavedDrive = Column(String(100), unique=False, nullable=False)
    WoodDeckSF = Column(Integer, unique=False, nullable=False)
    OpenPorchSF = Column(Integer, unique=False, nullable=False)
    EnclosedPorch = Column(Integer, unique=False, nullable=False)
    ThreeSeasonPorch = Column(Integer, unique=False, nullable=False)
    ScreenPorch = Column(Integer, unique=False, nullable=False)
    PoolArea = Column(Integer, unique=False, nullable=False)
    PoolQC = Column(String(100), unique=False, nullable=False)
    Fence = Column(String(100), unique=False, nullable=False)
    MiscFeature = Column(String(100), unique=False, nullable=False)
    PredictedPrice = Column(Float, unique=False, nullable=False)

    def __repr__(self):
        tweet_repr = "<UsageLog=(Usage_id='%s>"
        return tweet_repr % (self.Usage_id)


def create_db(args):
    """Creates a database with the data models inherited from `Base` (Usage_Log).

    Args:
        args: Argparse args - include args args.where and args.manual.

    Returns:
        None
    """
    logger.debug('Running the create_db function')
    
    if args.where == "Local":
        try:
            logger.info('Creating a local database at {}'.format(config.SQLALCHEMY_DATABASE_URI))
            engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
            logger.debug('Database engine successfully created.')            
        except Exception as e:
            logger.error(e)
            
    elif args.where == "AWS":
        try:
            
            if args.manual == "yes":
                logger.info('Creating an RDS database based on user input.')
                conn_type = "mysql+pymysql"
                user = input("USER:")
                password = getpass.getpass("PASSWORD:")
                host = input("RDS_ENDPOINT:")
                port = input("PORT:")
                db_name = input("DATABASE_NAME:")
                engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, db_name)
            
            else:
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
            Base.metadata.create_all(engine)
            logger.info('Database successfully created.')            
    
        except Exception as e:
            logger.error("Database could not be created. Kindly check the configurations and try again.")
            logger.error(e)
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Run components of the log usage data code")
    subparsers = parser.add_subparsers()
    
    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create_db", description="Create database to track usage logs")
    sb_create.add_argument("--where", default="Local", help="'Local' or 'AWS'")
    sb_create.add_argument("--manual", default="no", help="Set as 'yes' if manually inputing RDS db credentials. Seeks variables from environment by default")
    sb_create.set_defaults(func=create_db)

    args = parser.parse_args()
    args.func(args)
