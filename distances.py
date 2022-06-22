import math

def distanceBetween(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2

    c = 2 * math.asin(math.sqrt(a))

    r = 6371    # Radius of earth in kilometers

    return (c * r)

# def distToGPS(distance, currLat, currLon):
#     currLat = math.radians(removeFactor(currLat))
#     currLon = math.radians(removeFactor(currLon))

#     dlon = 0 # so vai variar a latitude

#     r = 6371

#     c = distance / (r * 10**3)

#     a = (math.sin(a**2)) / 2

#     1 / (a - math.acos(currLat) * math.acos(nextLat) * math.asin(dlon * 2)**-2) = math.asin(dlat * 2)**2 # dlat = ?


#     nextLat = currLat + dlat
#     nextlon = currLon + dlon

#     return(nextLat, nextlon)

# def metersPlusLatitude(meters, lat):
#     dist = 0
#     lat2 = lat
#     while(dist < meters):
#         lat2 += 1
#         dist = distanceBetween(lat, 0, lat2, 0)
#     return lat2

def metersToLatitude(meters):
    lat1 = 0
    lat2 = 0
    dist = 0
    while(dist < meters):
        lat2 += 1
        dist = distanceBetween(lat1, 0, lat2, 0)
    return lat2

latitude = 40.0000000
longitude = -8.0000000
latitude2 = 40.0000090
longitude2 = -8.0000000

# Tests
dist = distanceBetween(latitude, longitude, latitude2, longitude2)
print(dist)

lat1m = metersToLatitude(1)
print(lat1m)