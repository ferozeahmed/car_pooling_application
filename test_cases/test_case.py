import sys
import os
import json
from bson import ObjectId
import pytest
from unittest.mock import patch
from unittest.mock import Mock

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.handlers.car_pool_service import (Ride, User,
    update_user_in_db, create_user_in_db, get_user_by_id, 
    delete_user_in_db, create_ride_in_db, get_ride_by_id,
    find_rides_by_lat_lon, update_riders_in_db, connect_mongo
)


from app.handlers.dist_calc_service import haversine, find_nearest


# Test function
def test_connect_mongo(mocker):
    # Create a mock app with state and db attributes
    mock_db = Mock()
    mock_state = Mock()
    mock_state.db = mock_db
    mock_app = Mock()
    mock_app.state = mock_state
    
    # Use mocker to patch the 'main.app' with our mock_app
    mocker.patch('main.app', mock_app)
    
    # Call the function to test
    result = connect_mongo()
    
    # Check that the returned db is the mocked db
    assert result == mock_db


@patch('app.handlers.car_pool_service.connect_mongo')
def test_create_user_in_db(mock_connect_mongo):
    # Mock the connect_mongo function
    mock_db = mock_connect_mongo.return_value
    mock_collection = mock_db.__getitem__.return_value

    # Create a user object
    user = User(
        first_name='John',
        last_name='Doe',
        mail_id='john.doe@example.com',
        mobile='1234567890',
        address='123 Main St',
        latitude='37.1234',
        longitude='-122.5678',
        vehicle=[]
    )

    # Call the create_user_in_db function
    result = create_user_in_db(user)

    # Assert that the insert_one method was called with the user object
    mock_collection.insert_one.assert_called_once_with(user.dict())

    # Assert that the inserted_id is returned
    assert result == mock_collection.insert_one.return_value.inserted_id


@patch('app.handlers.car_pool_service.connect_mongo')
def test_get_user_by_id(mock_connect_mongo):
    # Mock the connect_mongo function
    mock_db = mock_connect_mongo.return_value
    mock_collection = mock_db.__getitem__.return_value
    
    # Define the expected result
    expected_result = {
        'first_name': 'John',
        'last_name': 'Doe',
        'mail_id': 'john.doe@example.com',
        'mobile': '1234567890',
        'address': '123 Main St',
        'latitude': 37.1234,
        'longitude': -122.5678,
        'vehicle': []
    }
    
    # Mock find_one to return the expected dictionary
    mock_collection.find_one.return_value = dict(sorted(expected_result.items()))


    # Call the get_user_by_id function
    result = get_user_by_id('john.doe@example.com')
    result = json.loads(result)

    # Assert that the find_one method was called with the correct arguments
    mock_collection.find_one.assert_called_once_with({"mail_id": 'john.doe@example.com'})

    # Assert that the result is equal to the expected result
    assert result == expected_result


@patch('app.handlers.car_pool_service.connect_mongo')
def test_update_user_in_db(mock_connect_mongo):
    # Mock the connect_mongo function
    mock_db = mock_connect_mongo.return_value
    mock_collection = mock_db.__getitem__.return_value

    # Create a user object
    user = User(
        first_name='John',
        last_name='Doe',
        mail_id='john.doe@example.com',
        mobile='1234567890',
        address='123 Main St',
        latitude='37.1234',
        longitude='-122.5678',
        vehicle=[]
    )

    # Call the update_user_in_db function
    result = update_user_in_db(user, 'john.doe@example.com')

    # Assert that the update_one method was called with the correct arguments
    mock_collection.update_one.assert_called_once_with(
        {"mail_id": 'john.doe@example.com'},
        {
            "$set":
                {
                    "first_name": 'John',
                    "last_name": 'Doe',
                    "mail_id": 'john.doe@example.com',
                    "mobile": '1234567890',
                    "address": '123 Main St',
                    "latitude": float('37.1234'),
                    "longitude": float('-122.5678'),
                    "vehicle": []
                }
        }
    )

    # Assert that the modified_count is returned
    assert result == mock_collection.update_one.return_value.modified_count



@patch('app.handlers.car_pool_service.connect_mongo')
def test_delete_user_in_db(mock_connect_mongo):
    # Mock the connect_mongo function
    mock_db = mock_connect_mongo.return_value
    mock_collection = mock_db.__getitem__.return_value

    # Call the delete_user_in_db function
    result = delete_user_in_db('john.doe@example.com')

    # Assert that the delete_one method was called with the correct arguments
    mock_collection.delete_one.assert_called_once_with({"mail_id": 'john.doe@example.com'})

    # Assert that the deleted_count is returned
    assert result == mock_collection.delete_one.return_value.deleted_count
    



@patch('app.handlers.car_pool_service.connect_mongo')
@patch('app.handlers.car_pool_service.get_user_by_id')
def test_create_ride_in_db(mock_get_user_by_id, mock_connect_mongo):
    # Mock the connect_mongo function
    mock_db = mock_connect_mongo.return_value
    mock_collection = mock_db.__getitem__.return_value

    # Mock the get_user_by_id function
    mock_user = {
        'latitude': 37.1234,
        'longitude': -122.5678
    }
    mock_get_user_by_id.return_value = mock_user

    # Define the input values
    mail_id = 'test@gmail.com'
    date = '2022-01-01T00:00:00.000Z'
    destination = 'Test Destination'
    seats_offered = 2
    vehicle_type = 'Car'

    # Call the create_ride_in_db function
    result = create_ride_in_db(mail_id, date, destination, seats_offered, vehicle_type)

    # Assert that the get_user_by_id method was called with the correct arguments
    mock_get_user_by_id.assert_called_once_with(mail_id)

    # Assert that the insert_one method was called with the correct arguments
    mock_collection.insert_one.assert_called_once_with({
        'mail_id': mail_id,
        'latitude': mock_user['latitude'],
        'longitude': mock_user['longitude'],
        'destination': destination,
        'seats_offered': seats_offered,
        'riders': [],
        'date': date,
        'status': 'scheduled',
        'vehicle': vehicle_type
    })

    # Assert that the inserted_id is returned
    assert result == mock_collection.insert_one.return_value.inserted_id



@patch('app.handlers.car_pool_service.connect_mongo')
def test_get_ride_by_id(mock_connect_mongo):
    # Mock the connect_mongo function
    mock_db = mock_connect_mongo.return_value
    mock_collection = mock_db.__getitem__.return_value

    # Define the expected result
    expected_result = [
        {
            'mail_id': 'test@gmail.com',
            'status': 'scheduled',
            'riders': ['rider1', 'rider2']
        },
        {
            'mail_id': 'test2@gmail.com',
            'status': 'scheduled',
            'riders': ['rider3']
        }
    ]

    # Mock find method to return the expected list
    mock_collection.find.return_value = expected_result

    # Call the get_ride_by_id function
    result = get_ride_by_id('test@gmail.com', 'scheduled')
    result = json.loads(result)
    # Assert that the find method was called with the correct arguments
    mock_collection.find.assert_called_once_with({
        "$or": [
            {
                "mail_id": 'test@gmail.com',
                "status": 'scheduled'
            },
            {
                "riders": 'test@gmail.com',
                "status": 'scheduled'
            }
        ]
    })

    # Assert that the result is equal to the expected result
    assert result == expected_result


@patch('app.handlers.car_pool_service.connect_mongo')
def test_find_rides_by_lat_lon(mock_connect_mongo):
    # Mock the connect_mongo function
    mock_db = mock_connect_mongo.return_value
    mock_collection = mock_db.__getitem__.return_value

    # Define the input values
    lat = 12.9715987
    lon = 77.5945627
    mail_id = 'test@gmail.com'
    destination = 'Test Destination'
    date = '2022-01-01T00:00:00.000Z'

    # Mock the collection.find method to return the expected rides
    mock_collection.find.return_value = [
        {
            'latitude': 14.9715987,
            'longitude': 77.5945627,
            'seats_offered': 2,
            'riders': ['rider1'],
            'date': '2022-01-01T00:00:00.000Z'
        },
        {
            'latitude': 13.9715987,
            'longitude': 79.5945627,
            'seats_offered': 1,
            'riders': ['rider2'],
            'date': '2022-01-01T00:00:00.000Z'
        }
    ]

    # Call the find_rides_by_lat_lon function
    result = find_rides_by_lat_lon(lat, lon, mail_id, destination, date)
    result = json.loads(result)

    expected_result = {
            'latitude': 14.9715987,
            'longitude': 77.5945627,
            'ride': {'latitude': 14.9715987, 
                    'longitude': 77.5945627, 
                    'seats_offered': 2, 
                    'riders': ['rider1'], 'date': '2022-01-01T00:00:00.000Z'
                    }
        }

    assert result == expected_result

@patch('app.handlers.car_pool_service.connect_mongo')
def test_update_riders_in_db(mock_connect_mongo):
    # Mock the connect_mongo function
    mock_db = mock_connect_mongo.return_value
    mock_collection = mock_db.__getitem__.return_value

    # Define the input values
    ride_id = ObjectId()
    user_mail_id = 'test@gmail.com'

    # Call the update_riders_in_db function
    result = update_riders_in_db(ride_id, user_mail_id)
    result = result[0]
    # Assert that the update_one method was called with the correct arguments
    mock_collection.update_one.assert_called_once_with(
        {"_id": ride_id},
        {
            "$push":
                {
                    "riders": user_mail_id
                }
        }
    )

    # Assert that the modified_count is returned
    assert result == mock_collection.update_one.return_value.modified_count



def test_haversine():
    # Test case 1: Distance between two same points should be 0
    assert haversine(12.9715987, 77.5945627, 12.9715987, 77.5945627) == 0

    # Test case 2: Distance between two different points
    assert haversine(12.9715987, 77.5945627, 13.9715987, 79.5945627) == pytest.approx(243.17, abs=0.1)

    # Test case 3: Distance between two different points
    assert haversine(12.9715987, 77.5945627, 11.9715987, 96.5945627) == pytest.approx(2065.37, abs=0.1)


def test_find_nearest():
    # Define the input values
    lat = 12.9715987
    lon = 77.5945627
    users = [
        {
            "latitude": 13.9715987,
            "longitude": 79.5945627
        },
        {
            "latitude": 14.9715987,
            "longitude": 77.5945627
        },
        {
            "latitude": 11.9715987,
            "longitude": 96.5945627
        }
    ]

    # Call the find_nearest function
    result = find_nearest(lat, lon, users)

    # Define the expected result
    expected_result = {
        "latitude": 14.9715987,
        "longitude": 77.5945627
    }

    # Assert that the result is equal to the expected result
    assert result == expected_result


if __name__ == '__main__':
    pytest.main()
