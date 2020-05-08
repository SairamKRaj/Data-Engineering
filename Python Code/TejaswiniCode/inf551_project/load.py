import requests
import MySQLdb
import json
import sys, traceback
import re

baseURL="https://projectinf551-6d437.firebaseio.com/"
wordSet=set()
stopwords={"a","an","the","of","for","and"}

def deleteJSON():

    try:

        # pathResponse = requests.delete(baseURL+"worldDB/city.json")
        # pathResponse1 = requests.delete(baseURL+"worldDB/country.json")
        # pathResponse2 = requests.delete(baseURL+"worldDB/countrylanguage.json")
        # pathResponse3 = requests.delete(baseURL+"worldDB/index.json")
        pathResponse4 = requests.delete(baseURL+"BABikeShare.json")
        pathResponse4 = requests.delete(baseURL+"BABikeShareIndex.json")

        print("Deleted old data")
    except:
            print("Upload exception" + sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)

def uploadJson(jsonData):
    print(jsonData)
    try:
        # print(jsonData)
        putResponse = requests.put(baseURL+"/BABikeShare/" + 'status.json', jsonData)
        print(putResponse.status_code)
        if putResponse.status_code == 200:
            print("Upload Successfull")
        else:
            print("Upload data failed")
    except:
        print("Upload exception" + sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)

def queryData():
    cityURL = baseURL + 'worldDB/city'+'.json'
    countryURL = baseURL + 'worldDB/country'+'.json'
    countryLangURL = baseURL + 'worldDB/countrylanguage'+'.json'

    cityResponse=requests.get(cityURL)
    cityJson=json.loads(cityResponse.text)

    countryResponse=requests.get(countryURL)
    countryJson=json.loads(countryResponse.text)

    countryLangResponse=requests.get(countryLangURL)
    countryLangJson=json.loads(countryLangResponse.text)

    jsonData={}

    for line in cityJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="city"
                        str1["COLUMN"]=key
                        str1["ID"]=line["ID"]
                        jsonData.setdefault(n, []).append(str1)


    for line in countryJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="country"
                        str1["COLUMN"]=key
                        str1["Code"]=line["Code"]
                        jsonData.setdefault(n, []).append(str1)

    for line in countryLangJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="countrylanguage"
                        str1["COLUMN"]=key
                        str1["CountryCode"]=line["CountryCode"]
                        jsonData.setdefault(n, []).append(str1)

    if(jsonData.__contains__("")):
        jsonData.pop("")

    test=json.dumps(jsonData).replace("'",'"')
    try:

        pathResponse = requests.patch(baseURL+"worldDBindex.json", test)
        # print(test)
        print(pathResponse.status_code)
        if pathResponse.status_code == 200:
            print("Index data upload Successfull")
        else:
            print("Upload data failed")
    except:
            print("Upload exception" + sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)

def queryData1():
    stationURL = baseURL + 'BABikeShare/station'+'.json'
    statusURL = baseURL + 'BABikeShare/status'+'.json'
    tripURL = baseURL + 'BABikeShare/trip'+'.json'

    stationResponse=requests.get(stationURL)
    stationJson=json.loads(stationResponse.text)

    statusResponse=requests.get(statusURL)
    statusJson=json.loads(statusResponse.text)

    tripResponse=requests.get(tripURL)
    tripJson=json.loads(tripResponse.text)

    jsonData={}

    for line in stationJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="station"
                        str1["COLUMN"]=key
                        str1["id"]=line["id"]
                        jsonData.setdefault(n, []).append(str1)


    for line in statusJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="status"
                        str1["COLUMN"]=key
                        str1["station_id"]=line["station_id"]
                        jsonData.setdefault(n, []).append(str1)

    for line in tripJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="trip"
                        str1["COLUMN"]=key
                        str1["id"]=line["id"]
                        jsonData.setdefault(n, []).append(str1)

    if(jsonData.__contains__("")):
        jsonData.pop("")

    test=json.dumps(jsonData).replace("'",'"')
    try:

        pathResponse = requests.patch(baseURL+"BABikeShareIndex.json", test)
        # print(test)
        print(pathResponse.status_code)
        if pathResponse.status_code == 200:
            print("Index data upload Successfull")
        else:
            print("Upload data failed")
    except:
            print("Upload exception" + sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)

def queryData2():
    answerURL = baseURL + 'statsQuestions/answers'+'.json'
    questionsURL = baseURL + 'statsQuestions/questions'+'.json'
    tagsURL = baseURL + 'statsQuestions/tags'+'.json'

    answerResponse=requests.get(answerURL)
    answerJson=json.loads(answerResponse.text)

    questionsResponse=requests.get(questionsURL)
    questionsJson=json.loads(questionsResponse.text)

    tagsResponse=requests.get(tagsURL)
    tagsJson=json.loads(tagsResponse.text)

    jsonData={}

    for line in answerJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="answers"
                        str1["COLUMN"]=key
                        str1["Id"]=line["Id"]
                        jsonData.setdefault(n, []).append(str1)


    for line in questionsJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="questions"
                        str1["COLUMN"]=key
                        str1["Id"]=line["Id"]
                        jsonData.setdefault(n, []).append(str1)

    for line in tagsJson:
        for key in line:
            is_matched=bool(re.match("[A-Za-z]+",str(line[key])))
            if (is_matched):
                name=re.sub('[^A-Za-z0-9 ]+', '', line[key])
                for n in name.split(" "):
                    n=n.lower()
                    if n not in stopwords:
                        str1={}
                        str1["TABLE"]="tags"
                        str1["COLUMN"]=key
                        str1["Id"]=line["Id"]
                        jsonData.setdefault(n, []).append(str1)

    if(jsonData.__contains__("")):
        jsonData.pop("")

    test=json.dumps(jsonData).replace("'",'"')
    try:

        pathResponse = requests.patch(baseURL+"statsQuestionsIndex.json", test)
        # print(test)
        print(pathResponse.status_code)
        if pathResponse.status_code == 200:
            print("Index data upload Successfull")
        else:
            print("Upload data failed")
    except:
            print("Upload exception" + sys.exc_info()[0])
            traceback.print_exc(file=sys.stdout)

# dbconn=MySQLdb.connect(database="mydb", user="root", password="tiger", host="localhost")
# query = "select * from status;"
#
# with dbconn.cursor(MySQLdb.cursors.DictCursor) as cursor:
#         cursor.execute(query)
#         data = cursor.fetchall()
#
# print (json.dumps(data,indent=4))
# res=json.dumps(data)
# uploadJson(res)
queryData2()
# deleteJSON()


