import configparser
import numpy as np
import time
import logging
import glob

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