from django.shortcuts import render
from django.http import HttpResponse
from .biodiversity.biodiversity_script_geolearn import find_animals_script
from .climate_change.time_lapse import time_lapse

# Create your views here.
def index( request ):
	return render( request, 'index.html' )

def brother( request ):
	return HttpResponse( "hell yeah, brother" )

def slides( request ):
	return render( request, 'Slides.html' )

def biodiversity_submit( request ):
	if request.method == 'POST':
		output = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
	else:
		output = 'Biodiversity Slideshow submission'
	#arguments = request.POST.get( 'param' )
	#print( arguments )
	find_animals_script( 35, -111 )
	#output = arguments
	return render( request, 'Slides.html', {'message': output} )

def climate_submit( request ):
	if request.method == 'POST':
		lat = request.POST.get('lat')
		lng = request.POST.get('long')

		time_lapse(lat, lng)
		output = "climate change script run successfully"

		return render( request, 'Slides.html', {'message': output} )
