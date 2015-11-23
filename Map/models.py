from django.db import models
from googlemaps import Client
from django.conf import settings
from datetime import datetime
import numpy as np


class LiquorLocation(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    avg_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def getRatings(self):
        ratingList = []
        for review in self.review_set.all():
            if review.rating > 0:
                ratingList.append(review.rating)
        return ratingList

    def get_average_rating(self):
        ratings = self.getRatings()
        if len(ratings) == 0:
            return "No user ratings"
        else:
            self.avg_rating = np.mean(ratings)
            self.save()
            return str(round(np.mean(ratings),1)) + " out of 5"

    def getPrices(self):
        pricingList = []
        for review in self.review_set.all():
            if review.price > -1:
                pricingList.append(review.price)
        return pricingList

    def average_price(self):
        prices = self.getPrices()
        if len(prices) == 0:
            return "No user pricing"
        else:
            return "$" + str(round(np.mean(prices),1))

    # Use Google Maps API Geocoding service to get the latitude/longitude for a certain address
    def get_lat_long(self):
        gmaps = Client(key=settings.GMAPS_API_KEY)
        results = gmaps.geocode(address=self.address + ", " + self.city, region="CA")
        if results:
            lat_lng = results[0]['geometry']['location']
            return lat_lng


class PrivateStore(LiquorLocation):
    pass


class BCLiquorStore(LiquorLocation):
    post_code = models.CharField(max_length=7)


class RuralAgencyStore(LiquorLocation):
    post_code = models.CharField(max_length=7)


class Review(models.Model):
    RATING_CHOICES = (

        (0,'N/A'),
        (1,'1'),
        (2,'2'),
        (3,'3'),
        (4,'4'),
        (5,'5'),
        )
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default= -1)

    store = models.ForeignKey(LiquorLocation, null=True)
    pub_date = models.DateTimeField('date published', default=datetime.now, blank=True)
    user_name = models.CharField(max_length=100, default="baka")

    comment = models.CharField(max_length=200, default = "")
    rating = models.IntegerField(choices=RATING_CHOICES, default = 0)

    class Meta:
        ordering = ['pub_date']



class Liquor(models.Model):
    category = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    size = models.DecimalField(max_digits=5, decimal_places=3)
    price = models.DecimalField(max_digits=7, decimal_places=2)


class BCLiquor(Liquor):
    pass


class PrivateLiquor(Liquor):
    store = models.ForeignKey(PrivateStore)



class RASLiquor(Liquor):
    store = models.ForeignKey(RuralAgencyStore)
