from pymongo import MongoClient
from bson.json_util import dumps, loads
import json
from bson import json_util
import re

def finding(regexp, colum):
    # Create the client
    client = MongoClient('localhost', 27017, waitQueueTimeoutMS=999999)

    # Connect to our database
    db = client['Ya_leaks']

    # Fetch our series collection
    series_collection = db['modifydata']

    query = "{ "+colum+" : { $regex: .*"+regexp+".* } }"
    query = { colum:{'$regex': '.*'+regexp+'.*'} }

    print(query)
    
    docs = series_collection.find(query)
    
    list_cur = list(docs)
    #print (list_cur[1])
    # Converting to the JSON
    json_data = json_util.dumps(list_cur, indent = 2)
    json_data = re.sub("[\n]", " ", json_data)
    try:    
        #json_data = parse_json(list_cur) 

        #print(json_data.encode('utf-8').decode('unicode-escape'))
        return(json_data.encode('utf-8').decode('unicode-escape'))
    except:
        print(f"Failed to load: {json_data}")
        return(f"Failed to load: {json_data}")
        
def parse_json(data):
    return json.loads(json_util.dumps(data, indent = 2))

def find_top():
    client = MongoClient('localhost', 27017)

    # Connect to our database
    db = client['Ya_leaks']

    # Fetch our series collection
    series_collection = db['data']

    collection = series_collection.collection_names()
    for collect in collection:
        print (collect)



def finding_phone(regexp):
    # Create the client
    client = MongoClient('localhost', 27017, waitQueueTimeoutMS=999999)

    # Connect to our database
    db = client['Ya_leaks']

    # Fetch our series collection
    series_collection = db['data_formated']
    query = { 'phone_number': int(regexp) }
    print(query)
    
    docs = series_collection.find(query)
    
    list_cur = list(docs)
    json_data = json_util.dumps(list_cur, indent = 2)
    try:    
        #print(f"{json_data}")
        return(json_data.encode('utf-8').decode('unicode-escape'))
    except:
        print(f"Failed to load: {json_data}")
        return(f"Failed to load: {json_data}")