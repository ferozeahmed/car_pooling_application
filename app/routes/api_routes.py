# This file contains the API routes for the application
import json
from fastapi import APIRouter
from app.models.requestModels import User
from app.handlers.car_pool_service import create_user_in_db
from app.handlers.car_pool_service import get_user_by_id
from app.handlers.car_pool_service import update_user_in_db
from app.handlers.car_pool_service import delete_user_in_db
from app.handlers.car_pool_service import create_ride_in_db
from app.handlers.car_pool_service import get_ride_by_id
from app.handlers.car_pool_service import find_rides_by_lat_lon
from app.handlers.car_pool_service import update_riders_in_db
from app.handlers.car_pool_service import update_ride_status_in_db

# create an instance of APIRouter
router = APIRouter()


# route to create users
@router.post("/users")
async def create_user(user: User):
    # use try catch block to handle exceptions
    try:
        # call the create_user function from car_pool_service
        # to create a user
        user_id = create_user_in_db(user)

    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}

    return {"message": f"User created successfully with id {user_id}"}


# route to get user by mail id
@router.get("/users/{mail_id}")
async def get_user(mail_id: str):
    # use try catch block to handle exceptions
    try:
        # call the get_user_by_id function from car_pool_service
        # to get a user by mail id
        user = get_user_by_id(mail_id)

        # if user is None, return a message
        if user is None:
            return {"message": "User not found"}

        # convert the user string to json
        user = json.loads(user)

    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}
    return user


# route to update user by id
@router.put("/users")
async def update_user(user: User):
    # use try catch block to handle exceptions
    try:
        # call the update_user_in_db function from car_pool_service
        # to update a user by mail id
        user_id = update_user_in_db(user, User.mail_id)
    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}

    return {"message": f"User with id {user_id} updated successfully"}


# route to delete user by id
@router.delete("/users/{mail_id}")
async def delete_user(mail_id: str):
    # use try catch block to handle exceptions
    try:
        # call the delete_user_in_db function from car_pool_service
        # to delete a user by mail id
        delete_user_in_db(mail_id)

    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}
    return {"message": f"User with id {mail_id} deleted successfully"}


# route to create rides
@router.post("/rides")
async def create_ride(mail_id: str, date: str, destination: str, seats_offered: int, vehicle_type: str):
    # use try catch block to handle exceptions
    try:
        # call the create_ride_in_db function from car_pool_service
        # to create a ride
        create_ride_in_db(mail_id, date, destination, seats_offered, vehicle_type)

    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}

    return {"message": "Ride created successfully"}


# route to get ride by id
@router.get("/rides/{mail_id}/{status}")
async def get_ride(mail_id: str, status: str):
    # use try catch block to handle exceptions
    try:
        # call the get_ride_by_id function from car_pool_service
        # to get a ride by mail id
        ride = get_ride_by_id(mail_id, status)

        if ride is None:
            return {"message": "Ride not found"}

        ride = json.loads(ride)

    except Exception as e:
        return {"message": f"An error occurred: {str(e)}"}

    return ride


# route to find ride for a user
@router.get("/rides/find/{mail_id}/{destination}/{date}")
async def find_ride(mail_id: str, destination: str, date: str):
    # use try catch block to handle exceptions
    try:
        # fetch the user details with mail id
        user = get_user_by_id(mail_id)
        user_json = json.loads(user)
        
        # call the find_ride function from car_pool_service
        # to find a ride for a user
        lat = user_json.get('latitude')
        lon = user_json.get('longitude')

        ride = find_rides_by_lat_lon(lat, lon, mail_id, destination, date)

        # if ride is None, return a message
        if ride is None:
            return {"message": "Ride not found"}

        ride = json.loads(ride)

    except:
        return {"message": "An error occurred"}

    return ride


# route to join a ride
@router.post("/rides/join")
async def join_ride(ride_id: str, mail_id: str):
    # use try catch block to handle exceptions
    try:
        # call the join_ride function from car_pool_service
        # to join a ride
        updated_count, ride_info = update_riders_in_db(ride_id, mail_id)

        # if updated count is greater than 0 then return Rider joined successfully.
        if updated_count > 0:
            return {
                        "message": "Ride joined successfully",
                        "ride": json.loads(ride_info)
                    }
        else:
            return {
                "message": "Ride not found"
            }

    except:
        return {"message": "An error occurred"}
    

# route to update ride status
@router.put("/rides/status")
async def update_ride_status(ride_id: str, status: str):
    # use try catch block to handle exceptions
    try:
        # call the update_ride_status function from car_pool_service
        # to update ride status
        update_ride_status_in_db(ride_id, status)

    except:
        return {"message": "An error occurred"}

    return {"message": "Ride status updated successfully"}

