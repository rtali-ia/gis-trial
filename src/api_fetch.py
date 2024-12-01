import numpy as np
import logging
import requests
import glob
import configparser
import time
from data_logger import setup_logger
from api_helper import read_api_settings, read_data_settings, write_settings, call_nasa_api

if __name__ == '__main__':
    
    # Set up logging
    logger = setup_logger('api_fetch.log')
    
    #Collect time statistics
    timer = []
    
    #Define BASE_PATH
    BASE_PATH = './data'
    
    #Read API settings from config.ini
    PATH = './config.ini'
    nasa_key, gibs_api, gibs_version, gibs_format, width, height, srs = read_api_settings(PATH)
    frequency, start_date, end_date = read_data_settings(PATH)
    write_path, mongo_db, mongo_uri = write_settings(PATH)
    
    #Read all locations from locations.csv, Skip header
    locs = np.genfromtxt('locations.csv', delimiter=',', dtype=str, encoding=None, skip_header=1)
    
    #Check if locs is a 1D array, Make it 2D
    if len(locs.shape) == 1:
        locs = [locs]
        
    #Read all channels from channels.csv
    channels = np.genfromtxt('channels.csv', delimiter=',', dtype=str, encoding=None, skip_header=1)
    
    #Calculate dates between start and end date using frequency in the YYYY-MM-DD format
    dates = np.arange(np.datetime64(start_date), np.datetime64(end_date), np.timedelta64(int(frequency), 'D'))
    dates = [str(date) for date in dates]
    
    # Call NASA API for each date
    
    for loc in locs:
        for channel in channels:
            for dt in dates:
                
                #Extract location details
                loc_cd, sw_lat, sw_lon, ne_lat, ne_lon = loc
                
                #Extract channel details
                channel_name = channel
                
                #Measure time taken to call API
                start_time = time.time()
                response = call_nasa_api(BASE_PATH, loc_cd, sw_lat, sw_lon, ne_lat, ne_lon, dt, channel_name, logger)
                end_time = time.time()
                time_seconds = end_time - start_time
                timer.append(time_seconds)
                
                if response:
                    logger.info(f'API call successful for location {loc}, channel {channel}, date {dt}. Time taken: {time_seconds}')
                else:
                    logger.error(f'API call failed for location {loc}, channel {channel}, date {dt}, Time taken: {time_seconds}')
    
    #Prepare Stats
    
    # Report the mean, sd and max time taken to call the API
    mean_time = np.mean(timer)
    sd_time = np.std(timer)
    max_time = np.max(timer)
    
    print(f'Mean time taken to call API: {mean_time}')
    print(f'Standard deviation of time taken to call API: {sd_time}')
    print(f'Max time taken to call API: {max_time}')
    
    logger.info(f'Mean time taken to call API: {mean_time}')
    logger.info(f'Standard deviation of time taken to call API: {sd_time}')
    logger.info(f'Max time taken to call API: {max_time}')
    
    # Done
    print('API fetch complete for all dates in range specified in config.ini file {start_date} to {end_date}')
    