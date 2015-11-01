from django.db import models
from googlemaps import Client, geocoding
from django.conf import settings

class LiquorLocation(models.Model):
    store_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.store_name

    # Use Google Maps API Geocoding service to get the latitude/longitude for a certain address
    def get_lat_long(self):
        gmaps = Client(key=settings.GMAPS_API_KEY)
        results = gmaps.geocode(self.address + ", " + self.city)
        if results:
            lat_lng = results[0]['geometry']['location']
            return lat_lng

class PrivateStore(LiquorLocation):
    pass


class BCLiquorStore(LiquorLocation):
    post_code = models.CharField(max_length=7)


class RuralAgencyStore(LiquorLocation):
    post_code = models.CharField(max_length=7)
