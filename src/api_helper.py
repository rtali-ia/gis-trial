import configparser
import numpy as np
import time
import logging
import glob
import requests
import os
from PIL import Image
from skimage.io import imread
import imageio.v3 as iio
from data_logger import setup_logger

def read_api_settings(PATH : str):
    # Read time settings from config file (./data.ini)
    config = configparser.ConfigParser()
    config.read(PATH)

    # Read two arrays from config file
    nasa_key = config.get('nasa_api','NASA_KEY')
    gibs_api = config.get('nasa_api','GIBS_API')
    gibs_version = config.get('nasa_api','GIBS_VERSION')
    gibs_format = config.get('nasa_api','FORMAT')
    width = config.get('nasa_api','WIDTH')
    height = config.get('nasa_api','HEIGHT')
    srs = config.get('nasa_api','SRS')

    return nasa_key, gibs_api, gibs_version, gibs_format, width, height, srs


def read_data_settings(PATH : str):
    # Read dataset settings from config file (./data.ini)
    config = configparser.ConfigParser()
    config.read(PATH)

    frequency = config.get('data_settings','FREQUENCY')
    start_date = config.get('data_settings','START_DATE')
    end_date = config.get('data_settings','END_DATE')
    
    return frequency, start_date, end_date

def write_settings(PATH : str):
    # Write dataset settings to config file (./data.ini)
    config = configparser.ConfigParser()
    config.read(PATH)

    write_path = config.get('write_settings','WRITE_PATH')
    mongo_db = config.get('write_settings','MONGO_DB')
    mongo_uri = config.get('write_settings','MONGO_URI')
    
    return write_path, mongo_db, mongo_uri


def call_nasa_api(base_folder, loc_cd, sw_lat, sw_lon, ne_lat, ne_lon, call_dt, mode, logger):
    #Create a bounding box
    extents = "{0},{1},{2},{3}".format(sw_lat, sw_lon, ne_lat, ne_lon)
    
    #Construct API URL
    gibs_url = 'https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?\
                    version=1.3.0&service=WMS&request=GetMap&\
                        format=image/png&STYLE=default&bbox={0}&CRS=EPSG:4326&\
                            HEIGHT=512&WIDTH=512&TIME={1}&layers={2}'.format(extents, call_dt, mode)

    #Call API to download png image and save it
    
    #Check if base folder exists
    if not os.path.exists(base_folder):
        os.mkdir(base_folder)
        
    #Check if location folder exists
    location_folder = os.path.join(base_folder, loc_cd)
    if not os.path.exists(location_folder):
        os.mkdir(location_folder)
        
    #Check if the mode folder exists
    mode_folder = os.path.join(location_folder, mode)
    if not os.path.exists(mode_folder):
        os.mkdir(mode_folder)
        
    #Call API to download image
    # Request and save image
    
    try:
        img_array = iio.imread(gibs_url)  # Read the image from the URL
        img = Image.fromarray(img_array)  # Convert to a PIL image
        img.save(os.path.join(mode_folder, 'img_{0}.png'.format(call_dt)))
        return True
    
    except Exception as e:
        logger.error(f'Error downloading image for {loc_cd} at {call_dt}: {e}')
        return False
    
    
    