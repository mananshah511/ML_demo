from flask import Flask
from housing.logger import logging
from housing.exception import HousingException
import sys

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def inex():
    try:
        raise Exception("We are testing custome exception")
    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message)
        logging.info("We are testing our logs files")
    return "This is demo for the machine learning Project"

if __name__=='__main__':
    app.run(debug=True)
