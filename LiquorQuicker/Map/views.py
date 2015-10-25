from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect


class MapView(TemplateView):
	"""
	A view of the Map
	"""
	template_name = 'Map/map.html'
