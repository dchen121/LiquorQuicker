from rest_framework import serializers
from Map.models import LiquorLocation, Review

class LiquorLocationSerializer(serializers.ModelSerializer):
	class Meta:
		model = LiquorLocation
		fields = ('id', 'name', 'address', 'city', 'latitude', 'longitude', 'avg_rating')

class ReviewSerializer(serializers.ModelSerializer):
	class Meta:
		model = Review
		fields = ('id', 'store', 'comment', 'rating', 'user_name')
