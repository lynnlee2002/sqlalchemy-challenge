# Dependencies
import numpy as np
import pandas as pd
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, distinct

# Import Flask
from flask import Flask, jsonify

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create an app
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    return (
        f"Welcome to my Climate App!<br/>"
        f"<br/>"
        f"Here are available routes:<br/>"
        f"<br/>"
        f"- 12 months of precipitation data: /api/v1.0/precipitation<br/>"
        f"<br/>"
        f"- JSON list of stations: /api/v1.0/stations<br/>"
        f"<br/>"
        f"- The dates and temperature observations of the most-active station for the previous year of data: /api/v1.0/tobs<br/>"
        f"<br/>"
        f"- Minimum, average, and maximum temperature for a specified star date (enter date in format YYYY-MM-DD): /api/v1.0/<start><br/>"
        f"<br/>"
        f"- Minimum, average, and maximum temperature for a start-end range (enter date in format YYYY-MM-DD): /api/v1.0/<start>/<end>"
    )


# 4. Define what to do when a user hits the /about route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database. 
    most_recent_data_point = dt.datetime(2017, 8, 23)

    # Calculate the date one year from the last date in data set.
    year_ago = most_recent_data_point - dt.timedelta(days=366) #2016 is a leap year

    # Perform a query to retrieve the date and precipitation scores
    date_prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_ago).all()

    # Close Session
    session.close()

    # Create a list for the data and precipitation data
    prcp_list = []
    for date, prcp in date_prcp_results:
        prcp_dict = {}
        prcp_dict[date] = prcp
        prcp_list.append(prcp_dict)
     
    # Display the precipitation data in JSON format
    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the station list
    station_list = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation)

    # Close Session
    session.close()

    # Create a list for the station data
    station_data = []
    for station, name, latitude, longitude, elevation in station_list:
        station_dict = {}
        station_dict['Station ID'] = station
        station_dict['Name'] = name
        station_dict['Latitude'] = latitude
        station_dict['Longitude'] = longitude
        station_dict['Elevation'] = elevation
        station_data.append(station_dict)

     # Display the precipitation data in JSON format
    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Starting from the most recent data point in the database. 
    most_recent_data_point = dt.datetime(2017, 8, 23)

    # Calculate the date one year from the last date in data set.
    year_ago = most_recent_data_point - dt.timedelta(days=366) #2016 is a leap year

    # Perform a query to retrieve the dates and temperature observations of the most-active station for the previous year of data.
    most_active_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= year_ago).all()

    # Close Session
    session.close()

    # Create a list to store the date and corresponding temperature
    temp_obs = []
    for date, tobs in most_active_station:
        temp_dict = {}
        temp_dict[date] = tobs
        temp_obs.append(temp_dict)
    
    # Display the precipitation data in JSON format
    return jsonify(temp_obs)

@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the minimum temperature, the average temperature, and the maximum temperature for a specified start date
    temperatures = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()

    # Close Session
    session.close()

    # Create a list to store the min, avg, and max temperatures
    start_date = []
    for min, avg, max in temperatures:
        min_max_avg = {}
        min_max_avg['Minimum Temperature'] = min
        min_max_avg['Average Temperature'] = avg
        min_max_avg['Maximum Temperature'] = max
        start_date.append(min_max_avg)

    # Display the precipitation data in JSON format
    return jsonify(start_date)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Perform a query to retrieve the minimum temperature, the average temperature, and the maximum temperature for a specified date range
    temperatures = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
  
    # Create a list to store the min, avg, and max temperatures
    start_end_date = []
    for min, avg, max in temperatures:
        min_max_avg = {}
        min_max_avg['Minimum Temperature'] = min
        min_max_avg['Average Temperature'] = avg
        min_max_avg['Maximum Temperature'] = max
        start_end_date.append(min_max_avg)

    # Display the precipitation data in JSON format
    return jsonify(start_end_date)

if __name__ == "__main__":
    app.run(debug=True)