import pymongo

# Create the client
client = MongoClient('localhost', 27017)

# Connect to our database
db = client['SeriesDB']

# Fetch our series collection
series_collection = db['series']