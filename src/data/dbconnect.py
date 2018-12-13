from __future__ import print_function
from sshtunnel import SSHTunnelForwarder
import mysql.connector
import configparser
from sqlalchemy import create_engine


def connect_with_config(path_to_config=None):
    config = configparser.ConfigParser()
    config.read(path_to_config)
    host = str(config['MYSQL']['address'])
    username_ssh = config['MYSQL']['address']
    password_ssh = config['MYSQL']['address']
    dbname = config['MYSQL']['dbname']
    host_mysql = config['MYSQL']['host_mysql']
    username_mysql = config['MYSQL']['username_mysql']
    password_mysql = config['MYSQL']['password_mysql']

    if host in ['127.0.0.1','localhost']:
        # return mysql.connector.connect(host=host, user=username_mysql, password=password_mysql, database=dbname)
        return (None,create_engine('mysql+mysqlconnector://%s:%s@%s/%s'%(username_mysql,password_mysql,host,dbname)))
        #return pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s'%(host,dbname,username_mysql,password_mysql))
    else:
        server = SSHTunnelForwarder(
            (config['MYSQL']['address'], 22),
            ssh_username=config['MYSQL']['username_ssh'],
            ssh_password=config['MYSQL']['password_ssh'],
            remote_bind_address=('127.0.0.1', 3306)
        )

        server.start()
        local_port = str(server.local_bind_port)
        engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s'%(username_mysql,password_mysql,host_mysql,local_port,dbname))

        return (server,engine)



if __name__ == '__main__':
    import os
    import pandas as pd
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config_path = dir_path+'/../../config.ini'
    (server,mysql_connection) = connect_with_config(config_path)
    print(server)
    print(mysql_connection)

    server.stop()