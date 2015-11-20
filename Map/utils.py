import numpy as np

def get_closest_points(lat, lng, locations):
    my_location = np.array([lat, lng])
    latLng = np.array(locations)
    latLng[:,1:] = latLng[:,1:] - my_location
    # getting the Euclidean distance from each point to our location
    latLng[:,1] = np.linalg.norm(latLng[:,1:],2,1)
    ind = np.argsort(latLng[:,1])
    # return closest fourth point so we can extend map bounds to that point
    # TODO: return list of sorted points so we can display list of locations sorted by distance
    return int(latLng[ind[4]][0])