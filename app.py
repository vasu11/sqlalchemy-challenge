import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
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
        f"/api/v1.0/tobs"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitations"""
    # Query all passengers
    #results = session.query(Measurement.name).all()
    precResults = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_precipitation = list(np.ravel(precResults))

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    stationResults = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(stationResults))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    yearAgoDate = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    """Return a list of temperatures for last year for a specific station"""
    # Query all passengers
    #stationResults = session.query(Station.station).all()
    precStation = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= yearAgoDate).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    prec_Station = list(np.ravel(precStation))

    return jsonify(prec_Station)


if __name__ == '__main__':
    app.run(debug=True)