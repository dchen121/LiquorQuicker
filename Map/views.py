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


class MapView(TemplateView):
    """
    A view of the Map
    """
    template_name = 'Map/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['geocode_locations'] = serializers.serialize("json", LiquorLocation.objects.filter(latitude__isnull=True))
        context['init_locations'] = serializers.serialize("json", LiquorLocation.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True))
        context['locations'] = serializers.serialize("json", LiquorLocation.objects.exclude(city__isnull=True))
        return context

def store_profile(request, pk):
    store = get_object_or_404(LiquorLocation, pk=pk)
    # most_recent = LiquorLocation.review_set.order_by('pub_date')

    ratings = LiquorLocation.getRatings(store);
    locations = serializers.serialize("json", LiquorLocation.objects.exclude(city__isnull=True))

    if request.user.is_authenticated():
        return render(request,'StoreProfile/authenticated_user.html',{'store':store, 'ratings':ratings, 'locations': locations, 'user': request.user, 'form':ReviewForm()})
    else:
        return render(request,'StoreProfile/anonymous_user.html',{'store':store, 'ratings':ratings, 'locations': locations, 'form':ReviewForm()})

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
        return redirect('map:store',pk)
    return render(request, 'StoreProfile/index.html', {'store': store, 'ratings':ratings, 'form': form})

def load_locations(request):
    top = None
    bottom = None
    right = None
    left = None
    
    if request.method == "GET":
        top = request.GET['top']
        bottom = request.GET['bottom']
        right = request.GET['right']
        left = request.GET['left']

        locations = LiquorLocation.objects.filter(
            latitude__gt=bottom
            ).filter(latitude__lt=top).filter(
            longitude__gt=left
            ).filter(longitude__lt=right)

        if locations.count() < 1:
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
        all_locations = LiquorLocation.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True).values_list('id', 'latitude', 'longitude')
        point = utils.get_closest_points(lat, lng, all_locations)
        locations = get_list_or_404(LiquorLocation, pk=point)

        return HttpResponse(serializers.serialize("json", locations), content_type='application/json')



        


