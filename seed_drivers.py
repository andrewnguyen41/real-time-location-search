from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['location_search']
drivers_collection = db['drivers']

# Sample driver data with coordinates in New York City
driver_data = [
    {'name': 'Driver 1', 'location': {'type': 'Point', 'coordinates': [-74.006, 40.7128]}},  # New York City
    {'name': 'Driver 2', 'location': {'type': 'Point', 'coordinates': [-73.995, 40.7178]}},  # Manhattan
    {'name': 'Driver 3', 'location': {'type': 'Point', 'coordinates': [-73.958, 40.7914]}},  # Upper East Side
]

# Insert sample drivers into the database
result = drivers_collection.insert_many(driver_data)
print(f"Inserted {len(result.inserted_ids)} drivers into the database.")

# create spatial index
drivers_collection.create_index([("location", "2dsphere")])
print(f"Created 2dsphere index.")
