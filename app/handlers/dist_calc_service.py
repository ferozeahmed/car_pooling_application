# find the nearest pair of latitude and longitude from the given latitude and longitude using haversine formula

from math import radians, sin, cos, sqrt, atan2


# https://en.wikipedia.org/wiki/Haversine_formula
def haversine(lat1, lon1, lat2, lon2):
    # convert latitude and longitude to radians
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))
    # calculate the difference between the latitude and longitude
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    # calculate the haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    # calculate the distance
    distance = 6371 * c
    return distance


def find_nearest(lat, lon, users):
    # create a list to store the distances and users with distances
    distances = []
    users_with_distances = []

    # iterate over the users list
    for user in users:
        # calculate the distance using haversine formula
        distance = haversine(lat, lon, user['latitude'], user['longitude'])
        # add the distance to the user's dictionary
        user_copy = user.copy()
        user_copy["distance_away"] = distance
        # append the user with distance to the list
        users_with_distances.append(user_copy)
        # append the distance to the list
        distances.append(distance)

    # find the index of the minimum distance
    index = distances.index(min(distances))
    # get the nearest user
    nearest_user = users_with_distances[index]

    # create a list of users within 5 km range
    users_within_5km = [user for user in users_with_distances if user["distance_away"] <= 5 and user != nearest_user]

    # combine the nearest user with users within 5 km range, with the nearest user on top
    result = [nearest_user] + users_within_5km

    # return the combined result
    return result

# lat = 12.9715987
# lon = 77.5945627
# users = [
#     {
#         "latitude": 13.9715987,
#         "longitude": 79.5945627
#     },
#     {
#         "latitude": 14.9715987,
#         "longitude": 77.5945627
#     },
#     {
#         "latitude": 11.9715987,
#         "longitude": 96.5945627
#     }
# ]
# nearest_users = find_nearest(lat, lon, users)
# print(nearest_users)
