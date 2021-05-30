from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

app = Flask(__name__)

# Import data from sqlite using SQLalhchemy. Use refelct to automate schema and class creation
engine = create_engine("sqlite:///Data/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)

# initialize the query tool
session = Session(engine)

# Create data tables with auto generated classes
Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def home():
    return(
        f"This API will return Hawaii Weather Data.<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations <br/>"
        f"/api/v1.0/tobs <br/>"
        f"/api/v1.0/startdate <br/>"
        f"/api/v1.0/startdate/enddate <br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return all precipitaion data in a list of dictionaries. 
    Uses the date as the key, and precipiation amount as the value"""

    # Query sqlite file to generate dataframe with precipitation data
    rainfall = pd.read_sql("""
    SELECT date AS Date, prcp As Precipitation
    FROM measurement 
    WHERE Date > DATE('2016-08-23')
    ORDER BY Date ASC;""",con = engine).dropna()

    # Create rainfall dictionary
    rainfalldict = {}
    for rows in rainfall.itertuples():
        rainfalldict[rows[0]] = ({rows[1]:rows[2]})
    
    #Return the results of the query in JSON format
    return(jsonify(rainfalldict))

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station).all()
    all_names = list(np.ravel(station_list))
    return(jsonify(all_names))

@app.route("/api/v1.0/tobs")
def tobs():
    with engine.connect() as data:
        mostactive = list(np.ravel(data.execute("""
        SELECT station
        FROM measurement
        GROUP BY station
        ORDER BY count(prcp) DESC
        LIMIT 1;
        """).all()))

    with engine.connect() as data:
        previous_year = data.execute("""
        SELECT date AS Date, tobs AS Temperature
        FROM measurement
        WHERE date > DATE('2016-08-23') and station = :ma;"""
        , {'ma':mostactive[0]}).all()    

    return(jsonify([dict(row) for row in previous_year]))

@app.route("/api/v1.0/<start>")
def start(start):
    with engine.connect() as data:
        tobs_stats = data.execute("""
        SELECT MIN(tobs) AS Temperature_Minimum,
        MAX(tobs) AS Temperature_Maximum,
        ROUND(AVG(tobs),0) AS Temperature_Average,
        MIN(date) AS Date_Beginning,
        MAX(date) AS Date_Ending
        FROM measurement
        WHERE date > :start;"""
        , {'start':start}).all()

    return(jsonify([dict(row) for row in tobs_stats]))

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    with engine.connect() as data:
        tobs_stats_se = data.execute("""
        SELECT MIN(tobs) AS Temperature_Minimum,
        MAX(tobs) AS Temperature_Maximum,
        ROUND(AVG(tobs),0) AS Temperature_Average,
        MIN(date) AS Date_Beginning,
        MAX(date) AS Date_Ending
        FROM measurement
        WHERE date >= :start AND date <= :end; """
        , {'start':start,'end':end}).all()

    return(jsonify([dict(row) for row in tobs_stats_se]))
    
if __name__ == "__main__":
    app.run(debug=True)