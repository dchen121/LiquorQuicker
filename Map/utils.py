from .models import LiquorLocation
import numpy as np
import math

# Adapted from https://gist.github.com/rochacbruno/2883505
# Haversine formula example in Python
# Author: Wayne Dyck

def distance(origin, destination):
    origin = np.radians(np.array(origin))
    destination = np.radians(np.array(destination))
    radius = 6371 # km

    delta = np.radians(destination - origin)
    a = np.square(np.sin(delta[:,0]/2)) + np.cos(np.radians(origin[0])) * np.cos(np.radians(origin[1])) * np.square(np.sin(delta[:,1]/2))
    c = 2 * np.arcsin(np.sqrt(a)) 
    d = radius * c

    return d

def calc_closest_points(lat, lng, locations):
    dist = distance((lat, lng), locations)
    ind = np.argsort(dist).tolist()
    return ind

def get_closest_points(lat, lng, locations, count):
    location_values = locations.values_list('latitude', 'longitude')
    ind = calc_closest_points(lat, lng, location_values)
    sorted_locations = []
    for i in range(0, count):
        sorted_locations.append(locations[ind[i]])

    return sorted_locations


