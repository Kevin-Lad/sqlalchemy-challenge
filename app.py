# Import the dependencies.
import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
   
    # Query precipitation analysis
    year_ago =  dt.date(2017, 8, 23) - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp). \
        filter(Measurement.date >= year_ago).all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of precripitation
    precipitation_list = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation_list.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():

    #Query the list of stations
    stations1 = session.query(Station.station).all()
    
    session.close()

    station_list = list(np.ravel(stations1))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    #Query the dates and temperature observations of the most active staions for the previous year
    most_active = 'USC00519281'
    year_ago =  dt.date(2017, 8, 23) - dt.timedelta(days=365)

    date_temp_results = session.query(Measurement.date, Measurement.tobs) \
                            .filter(Measurement.date >= year_ago) \
                            .filter(Measurement.station == most_active).all()

    date_temp_list = list(np.ravel(date_temp_results))

    return jsonify(date_temp_list)










if __name__ == '__main__':
    app.run(debug=True)