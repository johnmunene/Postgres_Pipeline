#!/usr/bin/env python
# coding: utf-8

# In[64]:


#loading necessary modules

#!pip install mysql-connector-python-rf
#!pip install mysql
import pandas as pd
import sqlite3
#import wget
import zipfile
from sqlalchemy import create_engine
import mysql.connector as sql


# In[66]:



#wget.download('https://bit.ly/3YNdO2Y')
unzipcsvfile = zipfile.ZipFile('./network_sensor.zip')

network_sensor_df = pd.read_csv(unzipcsvfile.open('network_sensor.csv'))
maintenance_df = pd.read_csv(unzipcsvfile.open('maintenance_records.csv'))
equipment_sensor_df = pd.read_csv(unzipcsvfile.open('equipment_sensor.csv'))


# In[67]:


#import pandas as pd


# # data cleaning

# In[68]:



def transform_data():
   
   
    #remove duplicate
    network_sensor_df.drop_duplicates()
    equipment_sensor_df.drop_duplicates()

    #remove null on time/date
    network_sensor_df2 = network_sensor_df.dropna(subset=['time', 'date'])
    equipment_sensor_df2 = equipment_sensor_df.dropna(subset=['time', 'date'])

    #replace null sensor reading with median value of the equipment id
    network_sensor_df2['sensor_reading'] = network_sensor_df2['sensor_reading'].fillna(network_sensor_df2['sensor_reading'].median())
    equipment_sensor_df2['sensor_reading'] = equipment_sensor_df2['sensor_reading'].fillna(equipment_sensor_df2['sensor_reading'].median())


    #rename columns to depicts their sensor reading and maintenance date and time
    network_sensor_df2.rename(columns = {'sensor_reading':'network_sensor_reading'}, inplace = True)
    equipment_sensor_df2.rename(columns = {'sensor_reading':'equipment_sensor_reading'}, inplace = True)
    maintenance_df.rename(columns = {'date':'maintenance_date','time':'maintenance_time' }, inplace = True)

    #merge the network and equipment sensor data as size, using ID,DATE,TIME
    sensor_df = pd.merge(network_sensor_df2, equipment_sensor_df2, how="left", on=["ID", "date", "time"])
    predict_df = pd.merge(sensor_df, maintenance_df, how="left", on=["ID"])
    data = predict_df
    return data


# # prediction

# In[69]:


def predict_maintenance(data):
    #write prediction code
    
    return data


# # load data to postgress

# In[70]:




def load_data(data):

    # create engine
    engine = create_engine('postgresql+psycopg2://john:Nevergiveup.1@104.154.64.203/test')

    #df to sql 
    #append(add the data), fail (nothing happens), replace(delete and create nee)
    #data2.to_sql =('sensor', engine, if_exists='replace', index= False)
    data.to_sql('maintenance_prediction', con=engine, if_exists='replace', index=False)


# In[71]:


data = transform_data()
data


# In[72]:


if __name__ == '__main__':
    
    data = transform_data()
    data = predict_maintenance(data)
    load_data(data)

