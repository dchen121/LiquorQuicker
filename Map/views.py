from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from Map.models import LiquorLocation, Review
from django.core import serializers
from .forms import ReviewForm
from datetime import datetime

class MapView(TemplateView):
    """
    A view of the Map
    """
    template_name = 'Map/homepage.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)
        context['geocode_locations'] = serializers.serialize("json", LiquorLocation.objects.filter(latitude__isnull=True))
        context['init_locations'] = serializers.serialize("json", LiquorLocation.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True))
        return context

def store_profile(request, pk):
    store = get_object_or_404(LiquorLocation, pk=pk)
    return render(request,'StoreProfile/index.html',{'store':store})

def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'Review/review_detail.html', {'review': review})

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'Review/review_list.html', context)

def add_review(request, pk):
    store = get_object_or_404(LiquorLocation, pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = form.cleaned_data['user_name']
        review = Review()
        review.store = store
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.now()
        review.save()
    return render(request, 'StoreProfile/index.html', {'store': store, 'form': form})


