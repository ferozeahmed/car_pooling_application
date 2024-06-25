# implementations
import json
from bson import ObjectId
from datetime import datetime, timedelta
from bson.json_util import dumps
from app.models.requestModels import User, Ride
from app.handlers.dist_calc_service import find_nearest


# function to connect the mongodb
def connect_mongo():
    # read the db from app state
    from main import app
    db = app.state.db
    return db


# function to create user in mongodb users collection
def create_user_in_db(user: User):
    db = connect_mongo()
    collection = db['users']
    result = collection.insert_one(user.dict())
    return result.inserted_id


# function to get user by id from mongodb users collection
def get_user_by_id(mail_id: str):
    db = connect_mongo()
    collection = db['users']
    result = collection.find_one({"mail_id": mail_id})
    return dumps(result)


# function to update user by id in mongodb users collection
def update_user_in_db(user: User, mail_id: str):
    db = connect_mongo()
    collection = db['users']

    # iterate over the vehicle list and convert it to dict
    vehicles = []
    for vehicle in user.vehicle:
        vehicles.append(vehicle.dict())

    result = collection.update_one(
        {"mail_id": mail_id},
        {
            "$set":
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "mail_id": user.mail_id,
                    "mobile": user.mobile,
                    "address": user.address,
                    "latitude": float(user.latitude),
                    "longitude": float(user.longitude),
                    "vehicle": vehicles
                }
        }
    )
    return result.modified_count


# function to delete user by id from mongodb users collection
def delete_user_in_db(mail_id: str):
    db = connect_mongo()
    collection = db['users']
    result = collection.delete_one({"mail_id": mail_id})
    return result.deleted_count


# function to create offer ride in mongodb rides collection
def create_ride_in_db(mail_id: str, date: str, destination: str, seats_offered: int, vehicle_type: str):
    db = connect_mongo()
    # fetch lat long from user
    user = get_user_by_id(mail_id)
    if isinstance(user, dict):  
        user = json.dumps(user)
    user_json = json.loads(user)
    latitude = user_json.get('latitude')
    longitude = user_json.get('longitude')

    # build the ride object
    ride = Ride(
        mail_id=mail_id, 
        latitude=latitude, 
        longitude=longitude, 
        destination=destination,
        seats_offered=seats_offered,
        riders=[],
        date=date,
        status="scheduled",
        vehicle=vehicle_type
    )

    collection = db['rides']
    result = collection.insert_one(ride.dict())
    return result.inserted_id


# function to get ride by id from mongodb rides collection
def get_ride_by_id(mail_id: str, status: str):
    db = connect_mongo()
    collection = db['rides']
    result = collection.find({
                                "$or": [
                                    {
                                        "mail_id": mail_id, 
                                        "status": status
                                    },
                                    {
                                        "riders": mail_id, 
                                        "status": status
                                    }
                                ]})

    # validate the result
    if result is None:
        return None
    
    # find if mail_id is present in riders list
    # and add is_rider key to the result
    rides = []
    for ride in result:
        if mail_id in ride['riders']:
            ride['is_rider'] = True
        else:
            ride['is_rider'] = False
        
        rides.append(ride)

    return dumps(rides)


# function to find rides for user from mongodb rides collection
def find_rides_by_lat_lon(lat: float, lon: float, mail_id: str, destination: str, date: str):
    # convert string to ISODate
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    print('iam here')
    # increase the datetime by 1 hour
    to_date = date + timedelta(hours=1)
    # convert the datetime to ISO format string
    to_date = to_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # decrease the datetime by 1 hour
    from_date = date - timedelta(hours=1)
    # convert the datetime to ISO format string
    from_date = from_date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    db = connect_mongo()
    collection = db['rides']
    # find the rides which are not completed and seats_offered is greater than 0
    # and mail_id is not equal to the user mail_id
    rides = collection.find(
            {
                "status": {"$ne": "completed"}, 
                "seats_offered": {"$gt": 0}, 
                "mail_id": {"$ne": mail_id},
                "destination": destination,
                "date": {"$gte": from_date, "$lte": to_date}
            }
        )
    
    # create a list to store the lat and lon of the rides
    lat_lon = []
    # iterate over the rides
    for ride in rides:
        # calculate the length of riders list
        riders = len(ride['riders'])
        # calculate the available seats
        available_seats = ride['seats_offered'] - riders
        # if available seats are greater than 0
        if available_seats > 0:
            address = json.loads(get_user_by_id(ride['mail_id'])).get('address')
            # append the lat and lon to the list
            lat_lon.append({"latitude": ride['latitude'], "longitude": ride['longitude'], "ride": ride,
                            "address": address})

    # if lat_lon is empty return message
    if not lat_lon:
        return None
    # find the nearest ride
    nearest_ride = find_nearest(lat, lon, lat_lon)
    return dumps(nearest_ride)


# function to update ride by id in mongodb rides collection
def update_riders_in_db(ride_id: str, user_mail_id: str):
    db = connect_mongo()
    collection = db['rides']

    # update riders info to the ride
    result = collection.update_one(
        {"_id": ObjectId(ride_id)},
        {
            "$push":
                {
                    "riders": user_mail_id
                }
        }
    )

    # fetch updated ride info and return
    ride_info = collection.find({
        "_id": ObjectId(ride_id)
    })
    return result.modified_count, dumps(ride_info)


# function to update ride status by id in mongodb rides collection
def update_ride_status_in_db(ride_id: str, status: str):
    db = connect_mongo()
    collection = db['rides']
    result = collection.update_one(
        {"_id": ObjectId(ride_id)},
        {
            "$set":
                {
                    "status": status
                }
        }
    )
    return result.modified_count