from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from Map.models import Location


class MapView(TemplateView):
    """
    A view of the Map
    """
    template_name = 'Map/map.html'

	def get_context_data(self, **kwargs):
		context = super(MapView, self).get_context_data(**kwargs)
		context['locations_list'] = Location.objects.all()
		return context
