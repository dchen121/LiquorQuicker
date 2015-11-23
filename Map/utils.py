from .models import LiquorLocation
import numpy as np

def calc_closest_points(lat, lng, locations):
    my_location = np.array([lat, lng])
    latLng = np.array(locations)
    latLng[:,1:] = latLng[:,1:] - my_location
    # getting the Euclidean distance from each point to our location
    latLng[:,1] = np.linalg.norm(latLng[:,1:],2,1)
    ind = np.argsort(latLng[:,1]).tolist()
    return ind

def get_closest_points(lat, lng, locations, count):
    location_values = locations.values_list('id', 'latitude', 'longitude')
    ind = calc_closest_points(lat, lng, location_values)
    sorted_locations = []
    print(locations)
    for i in range(0, count):
        sorted_locations.append(locations[ind[i]])

    return sorted_locations