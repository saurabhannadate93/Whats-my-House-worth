import pickle
import traceback
import os
import pandas as pd
import yaml
import datetime
from flask import Flask, render_template, request, redirect, url_for
import logging.config
from src.log_usage_data import usage_log
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger()

# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from flask_config.py
app.config.from_pyfile(os.path.join("..",'config','flask_config.py'))

# Initialize the database
db = SQLAlchemy(app)

@app.route('/')
def homepage():
    """Homepage of this system.
    
    Returns: rendered html template
    """
    logger.debug('homepage called.')
    #Trying to load the index page
    try:
        return render_template('homepage.html')
    except Exception as e:
        logger.error(e)
        return render_template('error.html')

@app.route('/index', methods=['POST','GET'])
def index():
    """Main view that get customer information for evaluation.
    
    Create view into evaluation page that allows to input information and predict price
    
    Returns: rendered html template
    """
    
    logger.debug('index called.')
    #Trying to load the index page
    try:
       return render_template('index.html')
    except Exception as e:
        logger.error(e)
        return render_template('error.html')

@app.route('/check', methods=['POST','GET'])
def check():
    """Function for predicting house price

    This function takes in the input data provided by the user and shows the predicted price
    
    Returns: rendered html template
    """
    logger.debug('check called.')
    #Retreiving inputs from the user input
    try:
        logger.debug("Start Retreiving Information.")
        
        GrLivArea = request.form['GrLivArea']
        GarageCars = request.form['GarageCars']
        TotalBsmtSF = request.form['TotalBsmtSF']
        YearBuilt = request.form['YearBuilt']
        FirstFlrSF = request.form['1stFlrSF']
        GarageArea = request.form['GarageArea']
        FullBath = request.form['FullBath']
        TotRmsAbvGrd = request.form['TotRmsAbvGrd']
        LotArea = request.form['LotArea']
        FirePlaces = request.form['FirePlaces']
        logger.debug("all inputs successfully retrieved.")

        if GrLivArea == '': GrLivArea = 0
        if GarageCars == '' : GarageCars = 0
        if TotalBsmtSF == '' : TotalBsmtSF = 0
        if YearBuilt == '' : YearBuilt = 0
        if FirstFlrSF == '' : FirstFlrSF = 0
        if GarageArea == '' : GarageArea = 0
        if FullBath == '' : FullBath = 0
        if TotRmsAbvGrd == '' : TotRmsAbvGrd = 0
        if LotArea == '' : LotArea = 0
        if FirePlaces == '' : FirePlaces = 0

    except Exception as e:
        logger.error(e)
        return render_template('error.html')
######################
    #Loading the model
    path = os.path.join(app.config['LOCAL_LOCATION'],app.config['MODEL_NAME'])
    with open(path, "rb") as f:
        model = pickle.load(f)
#######################

    logger.debug("Model successfully loaded. Creating predictions now.")
    try:
        Input_df = pd.DataFrame(columns=['GrLivArea', 'GarageCars', 'TotalBsmtSF', 'YearBuilt', '1stFlrSF', 'GarageArea', 
                        'FullBath', 'LotArea', 'TotRmsAbvGrd', 'Fireplaces'])
        Input_df.loc[0] = [GrLivArea, GarageCars, TotalBsmtSF, YearBuilt, FirstFlrSF, GarageArea, 
                        FullBath, LotArea, TotRmsAbvGrd, FirePlaces]
        
        pred_price = model.predict(Input_df)[0]

    except Exception as e:
        logger.error(e)
        return render_template('error.html')

    logger.debug("The predicted price is ${}".format(pred_price))

    logger.debug("Adding new record to database.")

    try:
        new_entry = usage_log(
            timestamp = str(datetime.datetime.now()),
            LotArea = LotArea,
            YearBuilt = YearBuilt,
            TotalBsmtSF = TotalBsmtSF,
            FirstFlrSF = FirstFlrSF,
            GrLivArea = GrLivArea,
            FullBath = FullBath,
            TotRmsAbvGrd = TotRmsAbvGrd,
            FirePlaces = FirePlaces,
            GarageCars = GarageCars,
            GarageArea = GarageArea,
            PredictedPrice = pred_price
        )

        db.session.add(new_entry)
        db.session.commit()
        logger.debug("New record added to the database")
        return render_template('index.html', predicted_price = pred_price)
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        return render_template('error.html')

def run_app(args):
    '''Runs the app
    
    Args:
        args: Argparse args - includes args.where, args.manual
        
    Returns:
        None
    '''
    logger.debug('Running the run_app function')

    with open(os.path.join("config","config.yml"), "r") as f:
        config = yaml.safe_load(f)

    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])

    

