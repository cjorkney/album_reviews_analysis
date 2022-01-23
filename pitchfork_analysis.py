import sqlite3
import numpy as np
import pandas as pd

#%% Constants

dbpath = 'data/database.sqlite'

# %% Get reviews data from database

# Establish connection to database
conn = sqlite3.connect(dbpath)

# Show tables in database
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#print(cursor.fetchall())

def make_query(table_name):
    return "SELECT * FROM " + table_name

reviews = pd.read_sql_query(make_query("reviews"), conn)
artists = pd.read_sql_query(make_query("artists"), conn)
genres = pd.read_sql_query(make_query("genres"), conn)
labels = pd.read_sql_query(make_query("labels"), conn)
years = pd.read_sql_query(make_query("years"), conn)
content = pd.read_sql_query(make_query("content"), conn)
