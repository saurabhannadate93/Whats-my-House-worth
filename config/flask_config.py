import os
MODE='Local' #'Local' or 'AWS' #change as necessary
BUCKET_NAME='nw-saurabhannadate-s3' #Necessary if MODE = 'AWS'

DEBUG = True
LOGGING_CONFIG = "config/logging_local.conf"

PORT = 3000
APP_NAME = "whats-my-house-worth"
HOST = "127.0.0.1"

conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'
if MODE == 'AWS':
    SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".\
    format(conn_type, user, password, host, port, DATABASE_NAME)
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/msia423.db'

SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False

MODEL_NAME='Random_Forest_v1.pkl'
MODEL_LOCATION="models"