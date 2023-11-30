from bson import ObjectId
from flask import Flask, render_template
from flask_socketio import SocketIO
from pymongo import MongoClient
from flask_socketio import emit

app = Flask(__name__, template_folder='./templates')
socketio = SocketIO(app)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["location_search"]
drivers_collection = db["drivers"]


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("update_location")
def update_location(data):
    driver_id = data["id"]
    new_lat = data["lat"]
    new_lon = data["lon"]

    result = drivers_collection.update_one(
        {"_id": ObjectId(driver_id)},
        {"$set": {"location": {"type": "Point", "coordinates": [new_lon, new_lat]}}},
    )
    
    if result.matched_count > 0:
        emit("update_location_success", {"message": "Location updated successfully"})
    else:
        emit("update_location_failure", {"message": "Failed to update location"}) 


@socketio.on("find_drivers")
def find_nearby_drivers(data):
    lat = data["lat"]
    lon = data["lon"]
    scan_distance = data["scan_distance"]

    # Perform a spatial query to find nearby drivers
    nearby_drivers = drivers_collection.find(
        {
            "location": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "$maxDistance": scan_distance,
                }
            }
        }
    )

    driver_list = [
        {"id": str(driver["_id"]), "location": driver["location"]["coordinates"]}
        for driver in nearby_drivers
    ]

    # Send the list of nearby drivers to the client
    emit("nearby_drivers", driver_list)


if __name__ == "__main__":
    socketio.run(app, debug=True)
