from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine,inspect,func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"This API will return weather Hawaii Weather Data.<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/startdate <br/>"
        f"/api/v1.0/startdate/enddate <br/>"
        )

@app.route("/api/v1.0/precipiation")
def precipitation():
    """Return all precipitaion data in a list of dictionaries. 
    Uses the date as the key, and precipiation amount as the value"""
    return('Precipiation Page')

@app.route("/api/v1.0/stations")
def stations():
    return(
        f""
        f""
        f""
    )

@app.route("/api/v1.0/tobs")
def stations():
    return(
        f""
        f""
        f""
    )

@app.route("/api/v1.0/<start>")
def stations():
    return(
        f""
        f""
        f""
    )

@app.route("/api/v1.0/<start>/<end>")
def stations():
    return(
        f""
        f""
        f""
    )
if __name__ == '__main__':
    app.run(debug=True)
