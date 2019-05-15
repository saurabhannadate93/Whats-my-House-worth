#Logging
LOGGER_NAME = 'root'

#Load Data Configurations
SOURCE_BUCKET = "housing-prices-data"

#Database Configurations
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/tracks.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False  # If true, SQL for queries made will be printed

#App Configuations
PORT = 3000
APP_NAME = "housing-prices"
HOST = "127.0.0.1"



