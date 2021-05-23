from flask import Flask, jsonify
import pandas as pd
from sqlalchemy import create_engine,inspect,func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd

app = Flask(__name__)

# Import data from sqlite using SQLalhchemy. Use refelct to automate schema and class creation
engine = create_engine("sqlite:///Data/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine,reflect = True)

# initialize the query tool
session = Session(engine)

# Create classes for each data table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create rainfall dictionary
rainfall = pd.read_sql("""
SELECT date AS Date, prcp As Precipitation
FROM measurement 
WHERE Date > DATE('2016-08-23')
ORDER BY Date ASC;""",con = engine).dropna()
rainfalldict = {}
for rows in rainfall.itertuples():
    rainfalldict[rows[0]] = ({rows[1]:rows[2]})

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

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return all precipitaion data in a list of dictionaries. 
    Uses the date as the key, and precipiation amount as the value"""
    return(jsonify(rainfalldict))



@app.route("/api/v1.0/stations")
def stations():
    return(session.query(Station.station))

#@app.route("/api/v1.0/tobs")
#def stations():
    # return(
       # f""
      #  f""
     #   f""
   # )

#@app.route("/api/v1.0/<start>")
#def stations():
    #return(
       # f""
      #  f""
     #   f""
    #)

#@app.route("/api/v1.0/<start>/<end>")
#def stations():
   # return(
    #    f""
     #   f""
      #  f""
    #)
if __name__ == '__main__':
    app.run(debug=True)
