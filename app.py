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
        f"/api/v1.0/start/end<br/>" 
        f"/api/v1.0/start<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
   
    # Query precipitation analysis
    recent_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    recent_date = dt.date.fromisoformat(recent_date_str)

    year_ago =  recent_date - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        all()
    
    session.close()
    
    # Create a dictionary from the row data and append to a list of precripitation
    prcp_dict ={}
    for result in results:
        date = result[0]
        prcp = result[1]
        prcp_dict[date] = prcp

    return jsonify(prcp_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    #Query the list of stations
    stations1 = session.query(Station.station).all()
    
    session.close()

    station_list = list(np.ravel(stations1))

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    #Query the dates and temperature observations of the most active staions for the previous year
    most_active = 'USC00519281'
    recent_date_str = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    recent_date = dt.date.fromisoformat(recent_date_str)

    year_ago =  recent_date - dt.timedelta(days=365)
   

    date_temp_results = session.query(Measurement.date, Measurement.tobs).\
                            filter(Measurement.date >= year_ago).\
                            filter(Measurement.station == most_active).\
                            all()

    date_temp_list = list(np.ravel(date_temp_results))

    return jsonify(date_temp_list)

@app.route("/api/v1.0/<start>/<end>")
def get_date(start, end):
    session = Session(engine)
    # Query temperatures(min, max and avg) between certain dates
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    group_by(Measurement.date).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()

    session.close()

    all_temps = []
    for date, min, avg, max in results:
        temp_dict = {}
        temp_dict['date'] = date,
        temp_dict['min'] = min,
        temp_dict['avg'] = avg,
        temp_dict['max'] = max
        all_temps.append(temp_dict)
    

    return jsonify(all_temps)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    # Query temperatures(min, max and avg) between certain dates
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    group_by(Measurement.date).\
    filter(Measurement.date >= start).\
    all()

    session.close()

    all_temps = []
    for date, min, avg, max in results:
        temp_dict = {}
        temp_dict['date'] = date,
        temp_dict['min'] = min,
        temp_dict['avg'] = avg,
        temp_dict['max'] = max
        all_temps.append(temp_dict)
    

    return jsonify(all_temps)

if __name__ == '__main__':
    app.run(debug=True)