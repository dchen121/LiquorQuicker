from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from Map.models import LiquorLocation, Review
from django.core import serializers
from .forms import ReviewForm
from datetime import datetime
from django.core.urlresolvers import reverse

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
    # most_recent = LiquorLocation.review_set.order_by('pub_date')
    return render(request,'StoreProfile/index.html',{'store':store,'form':ReviewForm()})


def add_review(request, pk):
    store = get_object_or_404(LiquorLocation, pk=pk)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.store = store
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.now()
        review.save()
        return redirect('map:store',pk)
    return render(request, 'StoreProfile/index.html', {'store': store, 'form': form})


