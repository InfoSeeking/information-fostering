import mysql.connector
import configparser

def connect_with_config(path_to_config=None):
    config = configparser.ConfigParser()
    config.read(path_to_config)