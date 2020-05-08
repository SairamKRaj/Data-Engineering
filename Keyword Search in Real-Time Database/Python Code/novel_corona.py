import json
import sys
import pandas as pd
import requests
import time
import numpy as np


pd.set_option('display.max_columns', None)


def delete_contents():
    requests.delete('https://inf551-dcbb6.firebaseio.com/novel_corona/patients.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/novel_corona/confirmed_cases.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/novel_corona/death_cases.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/novel_corona/recovered_cases.json')


def obtain_column_names():
    print(patientsDF.columns)
    print(confirmedcasesDF.columns)
    print(deathcasesDF.columns)
    print(recoveredcasesDF.columns)


def obtain_df_datatypes():
    print(patientsDF.info())
    print(confirmedcasesDF.info())
    print(deathcasesDF.info())
    print(recoveredcasesDF.info())


def drop_duplicates():
    print(patientsDF.shape)
    patientsDF.drop_duplicates(inplace=True)
    print(patientsDF.shape)

    print(confirmedcasesDF.shape)
    confirmedcasesDF.drop_duplicates(inplace=True)
    print(confirmedcasesDF.shape)

    print(deathcasesDF.shape)
    deathcasesDF.drop_duplicates(inplace=True)
    print(deathcasesDF.shape)

    print(recoveredcasesDF.shape)
    recoveredcasesDF.drop_duplicates(inplace=True)
    print(recoveredcasesDF.shape)


def obtain_null_counts():
    # # Data missing information - patientsDF
    data_info = pd.DataFrame(patientsDF.dtypes).T.rename(index={0: 'column type'})
    data_info = data_info.append(pd.DataFrame(patientsDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
    data_info = data_info.append(pd.DataFrame(patientsDF.isnull().sum() / patientsDF.shape[0] * 100).T.
                                 rename(index={0: 'null values (%)'}))
    print(data_info)

    # # Data missing information - confirmedcasesDF
    data_info = pd.DataFrame(confirmedcasesDF.dtypes).T.rename(index={0: 'column type'})
    data_info = data_info.append(pd.DataFrame(confirmedcasesDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
    data_info = data_info.append(pd.DataFrame(confirmedcasesDF.isnull().sum() / confirmedcasesDF.shape[0] * 100).T.
                                 rename(index={0: 'null values (%)'}))
    print(data_info)

    # # Data missing information - deathcasesDF
    data_info = pd.DataFrame(deathcasesDF.dtypes).T.rename(index={0: 'column type'})
    data_info = data_info.append(pd.DataFrame(deathcasesDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
    data_info = data_info.append(pd.DataFrame(deathcasesDF.isnull().sum() / deathcasesDF.shape[0] * 100).T.
                                 rename(index={0: 'null values (%)'}))
    print(data_info)

    # # Data missing information - recoveredcasesDF
    data_info = pd.DataFrame(recoveredcasesDF.dtypes).T.rename(index={0: 'column type'})
    data_info = data_info.append(pd.DataFrame(recoveredcasesDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
    data_info = data_info.append(pd.DataFrame(recoveredcasesDF.isnull().sum() / recoveredcasesDF.shape[0] * 100).T.
                                 rename(index={0: 'null values (%)'}))
    print(data_info)


# def rename_coulmns():
#     confirmedcasesDF.rename(columns = {'Province/State': 'id', 'Country/Region': 'owneruserid','Lat': 'creationdate','Long': 'score','1/22/20': 'title','Body': 'body'}, inplace=True, errors='coerce')



if __name__ == "__main__":
    start_time = time.time()

    # Read input data.
    patients_csv = sys.argv[1]
    confirmedcases_csv = sys.argv[2]
    deathcases_csv = sys.argv[3]
    recoveredcases_csv = sys.argv[4]

    # Attempt to delete already existing contents of the FireBase Database.
    try:
        delete_contents()
    except Exception:
        print("There is no access to the correct Firebase database. Please provide access before proceeding.")

    # Create the Dataframes.
    patientsDF = pd.read_csv(patients_csv)
    confirmedcasesDF = pd.read_csv(confirmedcases_csv)
    deathcasesDF = pd.read_csv(deathcases_csv)
    recoveredcasesDF = pd.read_csv(recoveredcases_csv)
    print("Creating Dataframes completed...")

    # Obtain columns names
    obtain_column_names()

    # Rename column names - cleaning data
    # rename_coulmns()

    confirmedcasesDF = pd.melt(frame=confirmedcasesDF, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name="recorded date", value_name="counts")
    confirmedcasesDF.rename(
        columns={'Province/State': 'province or state', 'Country/Region': 'county or region', 'Lat': 'latitude', 'Long': 'longitude'}, inplace=True, errors='coerce')

    deathcasesDF = pd.melt(frame=deathcasesDF, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                               var_name="recorded date", value_name="counts")
    deathcasesDF.rename(
        columns={'Province/State': 'province or state', 'Country/Region': 'county or region', 'Lat': 'latitude',
                 'Long': 'longitude'}, inplace=True, errors='coerce')

    recoveredcasesDF = pd.melt(frame=recoveredcasesDF, id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                               var_name="recorded date", value_name="counts")
    recoveredcasesDF.rename(
        columns={'Province/State': 'province or state', 'Country/Region': 'county or region', 'Lat': 'latitude',
                 'Long': 'longitude'}, inplace=True, errors='coerce')


    # # Obtain data types
    obtain_df_datatypes()
    #
    # # Convert to correct Data types.
    # obtain_correct_datatypes()
    #
    # # Obtain data types
    # obtain_df_datatypes()
    #

    # Drop Duplicates
    drop_duplicates()

    # # # Determine percentage of Null Values
    obtain_null_counts()

    # Load Firebase - patientsDF
    patientsDF.to_json("patientsDF.json", orient="records", date_format="epoch", double_precision=10,
                        force_ascii=True,
                        date_unit="ms", default_handler=None)
    data1 = json.load(open("patientsDF.json"))
    response = requests.put('https://inf551-dcbb6.firebaseio.com/novel_corona/patients.json', json=data1)
    print(response)
    patientsDF.to_csv("patients_clean.csv")

    # Load Firebase - confirmedcasesDF
    confirmedcasesDF.to_json("confirmedcasesDF.json", orient="records", date_format="epoch", double_precision=10,
                      force_ascii=True,
                      date_unit="ms", default_handler=None)
    data2 = json.load(open("confirmedcasesDF.json"))
    response = requests.put('https://inf551-dcbb6.firebaseio.com/novel_corona/confirmed_cases.json', json=data2)
    print(response)
    confirmedcasesDF.to_csv("confirmed_cases_clean.csv")

    # Load Firebase - deathcasesDF
    deathcasesDF.to_json("deathcasesDF.json", orient="records", date_format="epoch", double_precision=10,
                      force_ascii=True,
                      date_unit="ms", default_handler=None)
    data3 = json.load(open("deathcasesDF.json"))
    response = requests.put('https://inf551-dcbb6.firebaseio.com/novel_corona/death_cases.json', json=data3)
    print(response)
    deathcasesDF.to_csv("death_cases_clean.csv")

    # Load Firebase - recoveredcasesDF
    recoveredcasesDF.to_json("recoveredcasesDF.json", orient="records", date_format="epoch", double_precision=10,
                         force_ascii=True,
                         date_unit="ms", default_handler=None)
    data4 = json.load(open("recoveredcasesDF.json"))
    response = requests.put('https://inf551-dcbb6.firebaseio.com/novel_corona/recovered_cases.json', json=data4)
    print(response)
    recoveredcasesDF.to_csv("recovered_cases_clean.csv")



    # Calculate the total computation time of the program.
    end_time = time.time()
    print(f"Total duration of the program is: {end_time - start_time}")