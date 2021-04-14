from sqlalchemy import create_engine
import sqlite3
import pymysql
import pandas as pd

def get_conn():
    try:
        conn = sqlite3.connect("database")
        return conn
    except Exception as ex:
        print("get_conn", ex)
        return ex

def get_remote_conn(user, pas, IP, port):
    try:
        engine = create_engine("mysql+pymysql://{}:{}@{}/{}?host={}?port={}").format(user,pas,IP,user,IP,port)
        conn = engine.connect()
        return conn
    except Exception as ex:
        print(ex)
        return ex

def sql_execute(sentence):
    try:
        cursor = get_conn().cursor()
        return cursor.execute(sentence)
    except Exception as ex:
        print("sql_excute", ex)
        return ex

def pd_upload_csv(name : str, pth, head = 0):
    try:
        df = pd.read_csv(pth, header = head)
        frame = df.to_sql(name, get_conn(), if_exists = 'replace')
        return frame
    except Exception as ex:
        print(ex)
        return ex