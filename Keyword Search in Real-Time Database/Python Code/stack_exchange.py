import json
import sys
import pandas as pd
import requests
import time
import numpy as np
import chardet

pd.set_option('display.max_columns', None)


def delete_contents():
    requests.delete('https://inf551-dcbb6.firebaseio.com/stack_exchange/questions.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/stack_exchange/answers.json')
    requests.delete('https://inf551-dcbb6.firebaseio.com/stack_exchange/tags.json')


def obtain_column_names():
    print(questionsDF.columns)
    print(answersDF.columns)
    print(tagsDF.columns)


def determine_file_type():
    fq = open(questions_csv, "rb")
    result1 = chardet.detect(fq.read(10000))
    print(result1)

    fa = open(answers_csv, "rb")
    result2 = chardet.detect(fa.read(10000))
    print(result2)

    ft = open(tags_csv, "rb")
    result3 = chardet.detect(ft.read(10000))
    print(result3)


def rename_coulmns():
    questionsDF.rename(columns = {'Id': 'id', 'OwnerUserId': 'owneruserid','CreationDate': 'creationdate','Score': 'score','Title': 'title','Body': 'body'}, inplace=True, errors='coerce')
    answersDF.rename(columns = {'Id': 'id', 'OwnerUserId': 'owneruserid','CreationDate': 'creationdate','ParentId': 'parentid','Score': 'score','Body': 'body'}, inplace=True, errors='coerce')
    tagsDF.rename(columns = {'Id': 'id', 'Tag': 'tag'}, inplace=True, errors='coerce')


def obtain_df_datatypes():
    print(questionsDF.info())
    print(answersDF.info())
    print(tagsDF.info())


def obtain_correct_datatypes():
    questionsDF.creationdate = pd.to_datetime(questionsDF.creationdate, errors='coerce')
    answersDF.creationdate = pd.to_datetime(answersDF.creationdate, errors='coerce')


def clean_data():
    answersDF.creationdate = answersDF.creationdate.apply(lambda x: str(x).split()[0])
    answersDF.body = answersDF.body.apply(lambda x: str(x).replace("<p>", "").replace("</p>", ""))
    questionsDF.creationdate = questionsDF.creationdate.apply(lambda x: str(x).split()[0])
    questionsDF.body = questionsDF.body.apply(lambda x: str(x).replace("<p>", "").replace("</p>", ""))



def drop_duplicates():
    print(questionsDF.shape)
    questionsDF.drop_duplicates(inplace=True)
    print(questionsDF.shape)

    print(answersDF.shape)
    answersDF.drop_duplicates(inplace=True)
    print(answersDF.shape)

    print(tagsDF.shape)
    tagsDF.drop_duplicates(inplace=True)
    print(tagsDF.shape)


def obtain_null_counts():
    # Data missing information - questionsDF
    data_info = pd.DataFrame(questionsDF.dtypes).T.rename(index={0: 'column type'})
    data_info = data_info.append(pd.DataFrame(questionsDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
    data_info = data_info.append(pd.DataFrame(questionsDF.isnull().sum() / questionsDF.shape[0] * 100).T.
                                 rename(index={0: 'null values (%)'}))
    print(data_info)

    # # Data missing information - answersDF
    data_info = pd.DataFrame(answersDF.dtypes).T.rename(index={0: 'column type'})
    data_info = data_info.append(pd.DataFrame(answersDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
    data_info = data_info.append(pd.DataFrame(answersDF.isnull().sum() / answersDF.shape[0] * 100).T.
                                 rename(index={0: 'null values (%)'}))
    print(data_info)

    # # Data missing information - tagsDF
    data_info = pd.DataFrame(tagsDF.dtypes).T.rename(index={0: 'column type'})
    data_info = data_info.append(pd.DataFrame(tagsDF.isnull().sum()).T.rename(index={0: 'null values (nb)'}))
    data_info = data_info.append(pd.DataFrame(tagsDF.isnull().sum() / tagsDF.shape[0] * 100).T.
                                 rename(index={0: 'null values (%)'}))
    print(data_info)


if __name__ == "__main__":
    start_time = time.time()

    # Read input data.
    questions_csv = sys.argv[1]
    answers_csv = sys.argv[2]
    tags_csv = sys.argv[3]

    # Attempt to delete already existing contents of the FireBase Database.
    try:
        delete_contents()
    except Exception:
        print("There is no access to the correct Firebase database. Please provide access before proceeding.")
    exit(0)

    # Create the Dataframes.
    determine_file_type()
    questionsDF = pd.read_csv(questions_csv, encoding='ISO-8859-1')
    answersDF = pd.read_csv(answers_csv, encoding='ISO-8859-1')
    tagsDF = pd.read_csv(tags_csv, encoding='ISO-8859-1', nrows=120000)
    print("Creating Dataframes completed...")

    # Obtain columns names
    obtain_column_names()

    # Rename column names - cleaning data
    rename_coulmns()

    # Obtain column names after cleaning
    obtain_column_names()

    # Obtain data types
    obtain_df_datatypes()

    # Convert to correct Data types.
    obtain_correct_datatypes()

    # Obtain data types
    obtain_df_datatypes()

    # Drop Duplicates
    drop_duplicates()

    # # Determine percentage of Null Values
    obtain_null_counts()

    # Clean data content
    clean_data()

    # # Load Firebase - questions data.
    questionsDF.to_json("questionsDF.json", orient="records", date_format="epoch", double_precision=10, force_ascii=True,
                      date_unit="ms", default_handler=None)
    data1 = json.load(open("questionsDF.json"))
    response = requests.put('https://inf551-dcbb6.firebaseio.com/stack_exchange/questions.json', json=data1)
    print(response)
    questionsDF.to_csv("questions_clean.csv")

    # Load Firebase - answers data.
    answersDF.to_json("answersDF.json", orient="records", date_format="epoch", double_precision=10,
                        force_ascii=True,
                        date_unit="ms", default_handler=None)
    data2 = json.load(open("answersDF.json"))
    response = requests.put('https://inf551-dcbb6.firebaseio.com/stack_exchange/answers.json', json=data2)
    print(response)
    answersDF.to_csv("answers_clean.csv")

    # Load Firebase - tags data.
    tagsDF.id = tagsDF.id.astype(str).replace("'", "").replace("Â´s", "As").replace("§", "s").replace("Ã©",
                                                                                                        "A").replace(
        "Ã¨s", "As").replace(
        "(", "").replace(")", "").replace("Ã¯", "A").replace("©", "").replace("Ã³", "A").replace("Ã",
                                                                                                 "A").replace(
        "º", "o").replace("Ã-", "A").replace("Â–", "A").replace("Â", "A").replace("¤", "o").replace("[",
                                                                                                    "").replace(
        "]", "").replace("£", "").replace("-", " ").replace("Š", "S").replace("¢", "c").replace("-n",
                                                                                                "n").replace(
        "-a", "a").replace("C.", "C").replace("A´", "A").replace("-", " ").replace("/", " ").replace("±",
                                                                                                     "").replace(
        "š", "s").replace("A¨", "A").replace("¶", "").replace("°", "").replace("¦", "").replace("¬",
                                                                                                "").replace(
        "A–", "A").replace("¼", "").replace("œ", "").replace("«", "").replace("®", "").replace("¸", "").replace(
        "Ž", "Z").replace("‰", "").replace("¥", "").replace("–", " ").replace("½", "").replace("A…",
                                                                                               "A ").replace(
        "‡", " ").replace("A„l", "Al").replace("ª", "").replace("\'sR", "s R").replace("A’", "A").replace("A“",
                                                                                                          "A").replace(
        ", F", " F").replace(", 'F", "F").replace(", 'D", " 'D").replace(", 'U", " 'U")
    tagsDF.tag = tagsDF.tag.astype(str).replace("'", "").replace("Â´s", "As").replace("§", "s").replace("Ã©", "A").replace("Ã¨s", "As").replace(
                "(", "").replace(")", "").replace("Ã¯", "A").replace("©", "").replace("Ã³", "A").replace("Ã",
                                                                                                         "A").replace(
                "º", "o").replace("Ã-", "A").replace("Â–", "A").replace("Â", "A").replace("¤", "o").replace("[",
                                                                                                            "").replace(
                "]", "").replace("£", "").replace("-", " ").replace("Š", "S").replace("¢", "c").replace("-n",
                                                                                                        "n").replace(
                "-a", "a").replace("C.", "C").replace("A´", "A").replace("-", " ").replace("/", " ").replace("±",
                                                                                                             "").replace(
                "š", "s").replace("A¨", "A").replace("¶", "").replace("°", "").replace("¦", "").replace("¬",
                                                                                                        "").replace(
                "A–", "A").replace("¼", "").replace("œ", "").replace("«", "").replace("®", "").replace("¸", "").replace(
                "Ž", "Z").replace("‰", "").replace("¥", "").replace("–", " ").replace("½", "").replace("A…",
                                                                                                       "A ").replace(
                "‡", " ").replace("A„l", "Al").replace("ª", "").replace("\'sR", "s R").replace("A’", "A").replace("A“",
                                                                                                                  "A").replace(
                ", F", " F").replace(", 'F", "F").replace(", 'D", " 'D").replace(", 'U", " 'U")
    tagsDF.to_json("tagsDF.json", orient="records", date_format="epoch", double_precision=10,
                      force_ascii=True,
                      date_unit="ms", default_handler=None)
    data3 = json.load(open("tagsDF.json"))
    try:
        response = requests.put('https://inf551-dcbb6.firebaseio.com/stack_exchange/tags.json', json=data3)
    except requests.exceptions.HTTPError as err:
        print(err)
    print(response)
    tagsDF.to_csv("tags_clean.csv")

    # Calculate the total computation time of the program.
    end_time = time.time()
    print(f"Total duration of the program is: {end_time - start_time}")