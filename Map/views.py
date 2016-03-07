from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect, HttpResponse, Http404
from Map.models import LiquorLocation, Review
from UserProfile.models import LQUser
from django.core import serializers
from .forms import ReviewForm
from datetime import datetime
from django.core.urlresolvers import reverse
from . import utils
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Map.serializers import LiquorLocationSerializer, ReviewSerializer

class MapView(TemplateView):
    """
    A view of the Map
    """
    template_name = 'Map/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['locations'] = serializers.serialize("json", LiquorLocation.objects.exclude(city__isnull=True))
        return context

def store_profile(request, pk):
    store = get_object_or_404(LiquorLocation, pk=pk)
    # most_recent = LiquorLocation.review_set.order_by('pub_date')

    locations = serializers.serialize("json", LiquorLocation.objects.exclude(city__isnull=True))
    latitude = store.latitude;
    longitude = store.longitude;
    address = store.address;
    average_rating = LiquorLocation.get_average_rating(store);

    if request.user.is_authenticated():
        return render(request,'StoreProfile/authenticated_user.html',{'store':store, 'average_rating': average_rating, 'locations': locations, 'user': request.user, 'form':ReviewForm()})
    else:
        return render(request,'StoreProfile/anonymous_user.html',{'store':store, 'average_rating': average_rating, 'locations': locations, 'form':ReviewForm()})

def add_review(request, pk):
    store = get_object_or_404(LiquorLocation, pk=pk)
    ratings = LiquorLocation.getRatings(store);
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        price = form.cleaned_data['price']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.store = store
        review.user_name = user_name
        review.rating = rating
        review.price = price
        review.comment = comment
        review.pub_date = datetime.now()
        review.save()
        #store.avg_rating = store.get_average_rating()
        #store.save()
        return redirect('map:store',pk)
    return render(request, 'StoreProfile/index.html', {'store': store, 'ratings':ratings, 'form': form})

def load_locations(request):
    top = None
    bottom = None
    right = None
    left = None

    if request.method == 'POST':
        min_rating = request.POST['minRating']
        sort_by_rating = request.POST['sortByRating']
        lat = request.POST['lat']
        lng = request.POST['lng']
        top = request.POST['top']
        bottom = request.POST['bottom']
        right = request.POST['right']
        left = request.POST['left']

        locations = LiquorLocation.objects.filter(
            latitude__gt=bottom
            ).filter(latitude__lt=top).filter(
            longitude__gt=left
            ).filter(longitude__lt=right)

        # filter by min. rating
        locations = locations.filter(avg_rating__gte=min_rating)

        # Javascript boolean turns into a string when passed into Python
        if (sort_by_rating == 'true'):
            # sort by recommended
            locations = locations.order_by('-avg_rating')
        else: 
            # sort by distance
            if (lat and lng):
                locations = utils.get_closest_points(float(lat), float(lng), locations, locations.count())

        if len(locations) < 1:
            raise Http404("No locations found in this area.")
        else:
            return HttpResponse(serializers.serialize("json", locations), content_type='application/json')


def filter_by_city(request, city):
    filtered_stores = LiquorLocation.objects.filter(city__iexact=city)
    context = {'city' : city, 'filtered_stores' : filtered_stores, 'locations' : serializers.serialize("json", LiquorLocation.objects.exclude(city__isnull=True))}
    return render(request, 'Map/filter_by_city.html', context)

def favourite_store(request):
    if request.method == "GET":
        user_id = request.GET['user']
        store_id = request.GET['store']

        user = get_object_or_404(LQUser, pk=user_id)
        user.favorite_store = get_object_or_404(LiquorLocation, pk=store_id)
        user.save()

    check = get_object_or_404(LQUser, pk=user_id)  
    return HttpResponse(check.favorite_store is not None)

def closest_points(request):
    if request.method == "GET":
        lat = float(request.GET['lat'])
        lng = float(request.GET['lng'])
        count = int(request.GET['count'])
        all_locations = LiquorLocation.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
        sorted_locations = utils.get_closest_points(lat, lng, all_locations, count)

        if len(sorted_locations) < 1:
            raise Http404("No results found")
        else:
            return HttpResponse(serializers.serialize("json", [sorted_locations[count-1]]), content_type='application/json')

@api_view(['GET'])
def location_list(request, format=None):
    if request.method == 'GET':
        locations = LiquorLocation.objects.all()
        serializer = LiquorLocationSerializer(locations, many=True)
        return Response(serializer.data)

    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def location_detail(request, pk, format=None):
    try:
        location = LiquorLocation.objects.get(pk=pk)
    except LiquorLocation.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        serializer = LiquorLocationSerializer(location)
        return Response(serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def review_list(request, format=None):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def location_review_list(request, pk, format=None):
    try:
        location = LiquorLocation.objects.get(pk=pk)
    except LiquorLocation.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        reviews = Review.objects.filter(store__pk=pk)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


