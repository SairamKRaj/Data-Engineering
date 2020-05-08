import json
import sys
import pandas as pd
import requests
import time
import numpy as np


pd.set_option('display.max_columns', None)


def delete_contents():
    requests.delete('https://inf551-dcbb6.firebaseio.com/sf-bikeshare/station.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/sf-bikeshare/status.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/sf-bikeshare/trip.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/sf-bikeshare/weather.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/novel_corona/patients.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/novel_corona/confirmed_cases.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/novel_corona/death_cases.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/novel_corona/recovered_cases.json')


# def obtain_column_names():
#     print(stationDF.columns)
#     print(statusDF.columns)
#     print(weatherDF.columns)
#     print(tripDF.columns)
#     # pass
#
#
# def obtain_df_datatypes():
#     print(stationDF.info())
#     print(statusDF.info())
#     print(weatherDF.info())
#     print(tripDF.info())
#     #pass
#
#
# def drop_duplicates():
#     print(stationDF.shape)
#     stationDF.drop_duplicates(inplace=True)
#     print(stationDF.shape)
#
#     print(statusDF.shape)
#     statusDF.drop_duplicates(inplace=True)
#     print(statusDF.shape)
#
#     print(weatherDF.shape)
#     weatherDF.drop_duplicates(inplace=True)
#     print(weatherDF.shape)
#
#     print(tripDF.shape)
#     tripDF.drop_duplicates(inplace=True)
#     print(tripDF.shape)
#
#
# def obtain_null_counts():
#     # # Data missing information - stationDF
#     data_info = pd.DataFrame(stationDF.dtypes).T.rename(index={0: 'column type'})
#     data_info = data_info.append(pd.DataFrame(stationDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
#     data_info = data_info.append(pd.DataFrame(stationDF.isnull().sum() / stationDF.shape[0] * 100).T.
#                                  rename(index={0: 'null values (%)'}))
#     print(data_info)
#
#     # # Data missing information - statusDF
#     data_info = pd.DataFrame(statusDF.dtypes).T.rename(index={0: 'column type'})
#     data_info = data_info.append(pd.DataFrame(statusDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
#     data_info = data_info.append(pd.DataFrame(statusDF.isnull().sum() / statusDF.shape[0] * 100).T.
#                                  rename(index={0: 'null values (%)'}))
#     print(data_info)
#
#     # # Data missing information - weatherDF
#     data_info = pd.DataFrame(weatherDF.dtypes).T.rename(index={0: 'column type'})
#     data_info = data_info.append(pd.DataFrame(weatherDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
#     data_info = data_info.append(pd.DataFrame(weatherDF.isnull().sum() / weatherDF.shape[0] * 100).T.
#                                  rename(index={0: 'null values (%)'}))
#     print(data_info)
#
#     # Data missing information - tripDF
#     data_info = pd.DataFrame(tripDF.dtypes).T.rename(index={0: 'column type'})
#     data_info = data_info.append(pd.DataFrame(tripDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
#     data_info = data_info.append(pd.DataFrame(tripDF.isnull().sum() / tripDF.shape[0] * 100).T.
#                                  rename(index={0: 'null values (%)'}))
#     print(data_info)
#
#
# def fill_null_values():
#     tripDF.zip_code = tripDF.zip_code.fillna(value = 0)
#     weatherDF.wind_dir_degrees = weatherDF.wind_dir_degrees.fillna(value = np.mean(weatherDF.wind_dir_degrees))
#     weatherDF.cloud_cover = weatherDF.cloud_cover.fillna(value=np.mean(weatherDF.cloud_cover))
#     weatherDF.precipitation_inches = weatherDF.precipitation_inches.fillna(value=np.mean(weatherDF.precipitation_inches))
#     weatherDF.max_gust_speed_mph = weatherDF.max_gust_speed_mph.fillna(value=max(weatherDF.max_gust_speed_mph))
#     weatherDF.mean_wind_speed_mph = weatherDF.mean_wind_speed_mph.fillna(value=np.mean(weatherDF.mean_wind_speed_mph))
#     weatherDF.max_wind_Speed_mph = weatherDF.max_wind_Speed_mph.fillna(value=max(weatherDF.max_wind_Speed_mph))
#     weatherDF.min_visibility_miles = weatherDF.min_visibility_miles.fillna(value=min(weatherDF.min_visibility_miles))
#     weatherDF.mean_visibility_miles = weatherDF.mean_visibility_miles.fillna(value=np.mean(weatherDF.mean_visibility_miles))
#     weatherDF.max_visibility_miles = weatherDF.max_visibility_miles.fillna(value=max(weatherDF.max_visibility_miles))
#     weatherDF.min_sea_level_pressure_inches = weatherDF.min_sea_level_pressure_inches.fillna(value=min(weatherDF.min_sea_level_pressure_inches))
#     weatherDF.mean_sea_level_pressure_inches = weatherDF.mean_sea_level_pressure_inches.fillna(value=np.mean(weatherDF.mean_sea_level_pressure_inches))
#     weatherDF.max_sea_level_pressure_inches = weatherDF.max_sea_level_pressure_inches.fillna(value=max(weatherDF.max_sea_level_pressure_inches))
#     weatherDF.min_humidity = weatherDF.min_humidity.fillna(value=min(weatherDF.min_humidity))
#     weatherDF.mean_humidity = weatherDF.mean_humidity.fillna(value=np.mean(weatherDF.mean_humidity))
#     weatherDF.max_humidity = weatherDF.max_humidity.fillna(value=max(weatherDF.max_humidity))
#     weatherDF.min_dew_point_f = weatherDF.min_dew_point_f.fillna(value=min(weatherDF.min_dew_point_f))
#     weatherDF.mean_dew_point_f = weatherDF.mean_dew_point_f.fillna(value=np.mean(weatherDF.mean_dew_point_f))
#     weatherDF.max_dew_point_f = weatherDF.max_dew_point_f.fillna(value=max(weatherDF.max_dew_point_f))
#     weatherDF.min_temperature_f = weatherDF.min_temperature_f.fillna(value=min(weatherDF.min_temperature_f))
#     weatherDF.mean_temperature_f = weatherDF.mean_temperature_f.fillna(value=np.mean(weatherDF.mean_temperature_f))
#     weatherDF.max_temperature_f = weatherDF.max_temperature_f.fillna(value=max(weatherDF.max_temperature_f))
#
#
# def obtain_correct_datatypes():
#     stationDF.installation_date = pd.to_datetime(stationDF.installation_date, errors='coerce')
#     statusDF.time = pd.to_datetime(statusDF.time, errors='coerce')
#     weatherDF.date = pd.to_datetime(weatherDF.date, errors='coerce')
#     weatherDF.precipitation_inches = pd.to_numeric(weatherDF.precipitation_inches, errors='coerce')
#     tripDF.start_date = pd.to_datetime(tripDF.start_date, errors='coerce')
#     tripDF.end_date = pd.to_datetime(tripDF.end_date, errors='coerce')
#     tripDF.zip_code = pd.to_numeric(tripDF.zip_code, errors='coerce')
#
#
if __name__ == "__main__":
    start_time = time.time()

    # # Read input data.
    # station_csv = sys.argv[1]
    # status_csv = sys.argv[2]
    # trip_csv = sys.argv[3]
    # weather_csv = sys.argv[4]

    # Attempt to delete already existing contents of the FireBase Database.
    try:
        delete_contents()
    except Exception:
        print("There is no access to the correct Firebase database. Please provide access before proceeding.")

    # # Create the Dataframes.
    # stationDF = pd.read_csv(station_csv)
    # statusDF = pd.read_csv(status_csv, nrows=5000)
    # tripDF = pd.read_csv(trip_csv)
    # weatherDF = pd.read_csv(weather_csv)
    # weatherDF.drop(labels="events", axis=1, inplace=True)
    # print("Creating Dataframes completed...")
    #
    # # Obtain columns names
    # obtain_column_names()
    #
    # # Obtain data types
    # obtain_df_datatypes()
    #
    # # Convert to correct Data types.
    # obtain_correct_datatypes()
    #
    # # Obtain data types
    # obtain_df_datatypes()
    #
    # # Drop Duplicates
    # drop_duplicates()
    #
    # # Determine percentage of Null Values
    # obtain_null_counts()
    #
    # # Determine percentage of Null Values
    # fill_null_values()
    #
    # # Determine percentage of Null Values
    # obtain_null_counts()
    #
    # # Load Firebase - Station data.
    # stationDF.to_json("station_data.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True,
    #                  date_unit="ms", default_handler=None)
    # data1 = json.load(open("station_data.json"))
    # response = requests.put('https://inf551-dcbb6.firebaseio.com/sf-bikeshare/station.json', json=data1)
    # print(response)
    # stationDF.to_csv("station_clean.csv")
    #
    # statusDF.to_json("statusDF.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True,
    #                  date_unit="ms", default_handler=None)
    # data2 = json.load(open("statusDF.json"))
    # response = requests.put('https://inf551-dcbb6.firebaseio.com/sf-bikeshare/status.json', json=data2)
    # print(response)
    # statusDF.to_csv("status_clean.csv")
    #
    # weatherDF.to_json("weatherDF.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True,
    #                  date_unit="ms", default_handler=None)
    # data3 = json.load(open("weatherDF.json"))
    # response = requests.put('https://inf551-dcbb6.firebaseio.com/sf-bikeshare/weather.json', json=data3)
    # print(response)
    # weatherDF.to_csv("weather_clean.csv")
    #
    # tripDF.to_json("tripDF.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True,
    #                   date_unit="ms", default_handler=None)
    # data4 = json.load(open("tripDF.json"))
    # response = requests.put('https://inf551-dcbb6.firebaseio.com/sf-bikeshare/trip.json', json=data4)
    # print(response)
    # tripDF.to_csv("trips_clean.csv")

    # Calculate the total computation time of the program.
    end_time = time.time()
    print(f"Total duration of the program is: {end_time - start_time}")