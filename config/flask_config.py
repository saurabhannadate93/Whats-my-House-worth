DEBUG = True
LOGGING_CONFIG = "config/logging_local.conf"

PORT = 3000
APP_NAME = "whats-my-house-worth"
HOST = "127.0.0.1"

SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/msia423.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False

MODEL_LOCATION='local' #local or AWS. Bucket name needs to be specified in case of AWS
BUCKET_NAME='nw-saurabhannadate-s3'
MODEL_NAME='Random_Forest_v1.pkl'
LOCAL_LOCATION="models"