from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from Map.models import LiquorLocation
from django.core import serializers


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