# What's my house worth?

## Team Members
#### Project lead: Saurabh Annadate
#### QA lead: [Tanya Tandon](https://github.com/TanyaTandon) 


## Index
<!-- toc -->

- [Project Charter](#project-charter)
- [Project Plan](#project-plan)
- [Repo structure](#repo-structure)
- [Running the application](#running-the-application)
  * [1. Initial setup](#1-initial-setup)
  * [2. Set up environment](#2-set-up-environment)
  * [3. Download the data](#3-download-the-data)
  * [4. Initialize the database](#4-initialize-the-database)
  * [5. Clean the data](#5-clean-the-data)
  * [6. Generate features](#6-generate-features)
  * [7. Train model](#7-train-model)
  * [8. Launch App](#8-launch-app)
- [Make All](#make-all)
- [Testing](#testing)
- [Logging](#logging)
- [Links To notebooks](#links-to-notebooks)
- [Acknowledgements](#acknowledgements)

## Project Charter

### Vision
Real estate agencies require accurate estimation of the price of a property to decide whether it is undervalued or not before making an investment decision. Individual home buyers also need an objective estimate of a home before buying. House pricing decisions are often subjective and can lead to bad investment decisions. Our vision is to develop a platform which would help estimate the price of a property based on certain property characteristics to help drive investment decisions, increase profits and reduce costs.


### Mission
Mission is to build an app which would help accurately predict the price of a property based on certain characteristics like property type, no. of floors, age etc. which can be deployed as a website as well as an Android/iOS app

### Success Criteria

**Model Criterion**: Our model is successful if the R-square evaluation metric exceeds 60%. 

**Desired Business Outcomes**: A Key Performance Indicator of the success of the app would be continual increase in it's adoption to drive business decisions by the various Real Estate agencies and individual customers. This would be a good indicator of the model's accuracy performance as well. The intention is to deploy the app at a particular location, and based on the performance expand to other areas.    

## Project Plan

### Theme: Develop and deploy a platform that helps estimate the valuation of a property based on certain characteristics. 

1. __EPIC 1: Model Building and Optimization__
    * Story 1 : Data Visualization
    * Story 2 : Data Cleaning and missing value imputation
    * Story 3 : Feature Generation
    * Story 4 : Testing different model architectures and parameter tuning
    * Story 5 : Model performance tests to check the model run times
   
2. __EPIC 2: Model Deployment Pipeline Development__
    * Story 1 : Environment Setup : requirement.txt files
    * Story 2 : Set up S3 instance
    * Story 3 : Initialize RDS database
    * Story 4 : Deploy model using Flask
    * Story 5 : Development of unit tests and integrated tests
    * Story 6 : Setup usage logs
    * Story 7 : Solution reproducibility tests
    
3. __EPIC 3: User Interface Development__
    * Story 1 : Develop a basic form to input data and output results
    * Story 2 : Add styling/colors to make the interface more visually appealing  

### Backlog

Sprint Sizing Legend:

* 0 points - quick chore
* 1 point ~ 1 hour (small)
* 2 points ~ 1/2 day (medium)
* 4 points ~ 1 day (large)
* 8 points - big and needs to be broken down more when it comes to execution (okay as placeholder for future work though)
------------------
* EPIC 2 : Story 2 : Set up a S3 instance (1) : Sprint 1 (Completed)
* EPIC 2 : Story 3 : Initialize RDS database(1) : Sprint 1 (Completed)
* EPIC 1 : Story 1 : Exploratory Data Analysis (2) : Sprint 1 (Completed)
* EPIC 1 : Story 2 : Data Cleaning and missing value imputation (2) : Sprint 1 (Completed)
* EPIC 2 : Story 1 : Environment Setup : requirement.txt files (1) : Sprint 1 (Completed)
* EPIC 1 : Story 3 : Feature Generation (2) : Sprint 2 (Completed)
* EPIC 1 : Story 4 : Testing different model architectures and parameter tuning (8) : Sprint 2 (Completed)
* EPIC 1 : Story 5 : Model performance tests (2) : Sprint 2 (Completed)
* EPIC 2 : Story 4 : Deploy model using Flask (2) : Sprint 2 (Completed)
* EPIC 2 : Story 5 : Development of unit tests and integrated tests (4) : Sprint 2 (Completed)
* EPIC 3 : Story 1 : Develop a basic form to input data and output results (2) : Sprint 2 (Completed)
* EPIC 2 : Story 6 : Setup usage logs (2) : Sprint 2 (Completed)
* EPIC 2 : Story 7 : Solution reproducibility tests (4) : Sprint 2 (Completed)

### IceBox 
* EPIC 3 : Story 2 : Add styling/colors to make the interface more visually appealing (Completed)

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── app.py                        <- Contains all the functionality of the flask app 
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging_local.conf            <- Configuration files for python loggers
│   ├── config.py                     <- Contains all configurations required for processing and set up
│   ├── flask_config.py               <- Contains all config required for the flask app
│
├── data                              <- Folder that contains data used or generated. Not tracked by git
│   ├── raw/                          <- Place to put raw data used for training the model 
│   ├── clean/                        <- Contains the cleaned dataset after the raw data has been cleaned
│   ├── features/                     <- Contains the data with the features
│
├── database                          <- Folder that contains the local SQLite database
│
├── deliverables                      <- Contains all deliverables for the project
│
├── logs                              <- Contains execution logs
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development
│   ├── deliver                       <- Notebooks shared with others 
│   ├── archive                       <- Developed notebooks no longer being used 
│
├── src                               <- Contains all the scripts for the project
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── load_data.py                  <- Script for downloading data from the input source 
│   ├── clean_data.py                 <- Script for cleaning the raw data
│   ├── features.py                   <- Script containing features that are required to be generated for modelling
│   ├── generate_features.py          <- Script that uses the features script to generate features
│   ├── log_usage_data.py             <- Script for building the usage log database and injesting data in it
│   ├── train_model.py                <- Script that trains the model using the final training data
│
├── tests                             <- Contains files for unit testing
│
├── run.py                            <- Simplifies the execution of one or more of the src scripts 
│
├── requirements.txt                  <- Python package dependencies 
│
├── Makefile                          <- Makefile to execute the make commands
```

## Running the application

Ths application can be run on both local system as well as on AWS. Steps on how to deploy the app for both settings is given below.

### 1. Initial Setup

Depending on where the app is deployed, ensure to go through the following:

#### Running on a local machine

**Specs**
* *Server: Local system*
* *Data Storage: Local filesystem*
* *Database: Local SQLite database*

**Makefile**
* Ensure that the `WHERE` variable is set to "Local"
* Ensure that the variable `BUCKET` is set to "Scripts" if running on Windows, else "bin" if on Linux or MacOS

**config/flask_config.py**
* Ensure that the `WHERE` variable is set to "Local"
* Ensure that the `HOST` variable is set to "127.0.0.1"
* Keep the default `PORT` of 3000; However, change it if this port is not available

**Setting up AWS CLI**
AWS CLI needs to be configured in your system for you to fetch the training data. Kindly refer to this [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) to set up the same  


#### Running on AWS

**Specs**
* *Server: EC2*
* *Data Storage: S3 bucket provided by the user*
* *Database: RDS MySQL database provided by the user*

**RDS configurations**
In order to use RDS, the RDS credentials need to be added to the os environment. Add the following variables to the environment:
* MYSQL_USER : *Username to access the RDS instance*
* MYSQL_PASSWORD : *Password to access the RDS instance*
* MYSQL_HOST : *RDS instance endpoinr*
* MYSQL_PORT : *Port number to access the instance*
* MYSQL_DB : *Name of the database*


**Makefile**
* Ensure that the `WHERE` variable is set to "AWS"
* Set the variable `STORAGE_S3_BUCKET` to the S3 bucket that you intend to use
* Ensure that the variable `BUCKET` is set to "Scripts" if running on Windows server, else "bin" if on Linux server

**config/flask_config.py**
* Ensure that the `WHERE` variable is set to "AWS"
* Ensure that the `HOST` variable is set to "0.0.0.0"


### 2. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv housePrices

source housePrices/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n housePrices python=3.7.3
conda activate housePrices
pip install -r requirements.txt

```

#### With `Make`

```bash
make venv
```


### 3. Download the data

Original Data Source: [Kaggle](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)

For the ease of downloading, the raw data has been downloaded and placed in a public s3 bucket: **s3://housing-prices-data** 


#### Running on Local
Run the following command in command line:
```bash
python run.py load_data
```

With `Make`
```
make load_data
```
Running this code will download the raw data from the s3 bucket and will put it in **/Data/raw/**


#### AWS
Run the following command in command line:
```bash
python run.py load_data --where=AWS --bucket=<destination_bucket_name>
```

With `Make`
```
make load_data
```
Running this code will download the raw data from the s3 bucket and will put it in **<destination_bucket_name>/raw/**


### 4. Initialize the database

#### Local
Run the following command in command line:
```bash
python run.py create_db
```

With `Make`
```
make create_db
```

Running this code will create a sqlite database to log the app usage at: **/Database/msia423.db**

#### AWS

Run the following command in command line:
```bash
python run.py create_db --where=AWS
```

With `Make`
```
make create_db
```

Running this code will create the database specified in the given RDS instance 


### 5. Clean the data

#### Local
Run the following command in command line:
```bash
python run.py clean_data
```

With `Make`
```
make clean_data
```
Running this code will clean the raw data and create a cleaned dataset at: **/Data/clean/**

#### AWS
Run the following command in command line:
```bash
python run.py clean_data --where=AWS --bucket=<destination_bucket_name>
```

With `Make`
```
make clean_data
```
Running this code will clean the raw data from the S3 bucket and will put it in **<destination_bucket_name>/clean/**


### 6. Generate features

#### Local
Run the following command in command line:
```bash
python run.py generate_features
``` 

With `Make`
```
make generate_features
```
Running this code will clean the raw data and create a cleaned dataset at: **/Data/clean/**

#### AWS
Run the following command in command line:
```bash
python run.py clean_data --where=AWS --bucket=<destination_bucket_name>
```

With `Make`
```
make generate_features
```
Running this code will clean the raw data from the S3 bucket and will put it in **<destination_bucket_name>/clean/**

### 7. Train Model

#### Local
Run the following command in command line:
```bash
python run.py train_model
``` 

With `Make`
```
make train_model
```
Running this code will train the prediction model and will dump it at: **/models/**

#### AWS
Run the following command in command line:
```bash
python run.py train_model --where=AWS --bucket=<destination_bucket_name>
```

With `Make`
```
make train_model
```
Running this code will clean the raw data from the S3 bucket and will put it in **<destination_bucket_name>/models/**

### 8. Launch app

#### Local or AWS
Run the following command in command line:
```bash
python run.py run_app
``` 

With `Make`
```
make app
```
Running this code will start the flask app at the IP specified in **config/flask_config.py**

## Make All

In order to use Make All, please ensure that the [Initial Setup](#1-initial-setup) is complete

Run the following command in command line:
```
make all
```

## Testing

In order to unit test the functions, follow the following steps:
1. Navigate to the tests folder
2. Run the following command on the command line:
```
pytest test_all_functions.py
```

## Logging
All logs are saved at **logs/logfile.log**




## Links to Notebooks
[Exploratory Data Analysis](notebooks/deliver/Exploratory_Data_Analysis.ipynb)

[Model Selection](notebooks/deliver/Data_Pre_Processing_and_Model_Selection.ipynb)

## Acknowledgements
Sincerest thanks:  
* Tanya Tandon
* Chloe Mawer
* Fausto Inestroza
* Xiaofeng Zhu









