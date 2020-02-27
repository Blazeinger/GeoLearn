from django.shortcuts import render
from django.http import HttpResponse
from .biodiversity.biodiversity_script_geolearn import find_animals_script
from .biodiversity.biodiversity_image_scraper import image_scraper
#from .climate_change.time_lapse import time_lapse
from subprocess import run,PIPE
import sys

# Create your views here.
'''
Views are the python function that are associated with different urls.
When you go to a URL in the 'urls.py', it will run the function in this script
In the urls script, you can see that the path '' is associated with the index
function just below. When you go to localhost with no extension, it will run
the index function.
If you go to localhost/brother, it will run the brother function.
'''
def index( request ):
	# render, the way I'm using it, just runs an html file.
	# It may do other things that I don't know, but that's what it's doing here
	return render( request, 'index.html' )

def brother( request ):
	return HttpResponse( "hell yeah, brother" )

def slides( request ):
	return render( request, 'Slides.html' )

def biodiversity_submit( request ):
	'''
	# For now, these don't matter. I do want to keep them here for future reference just in case
	if request.method == 'POST':
		output = 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'
	else:
		output = 'Biodiversity Slideshow submission'
	#arguments = request.POST.get( 'param' )
	#print( arguments )
	#image_scraper( 'fennec fox' )
	'''
	lat = request.POST.get( 'lat' )
	lng = request.POST.get( 'long' )
	
	#csv_filename = find_animals_script( lat, lng )
	
	
	
	output = lat
	return render( request, 'Slides.html', {'message': output} )

def climate_submit( request ):
	lat = request.POST.get('lat')
	lng = request.POST.get('long')

	out = run([sys.executable,
	'//mnt//c//Users//Samuel Prasse//Documents//GitHub//GeoLearn//GeoLearn App//GeoLearn-django_website//testsite//polls//climate_change//time_lapse.py', lat, lng], shell=False, stdout=PIPE)

	#time_lapse(lat, lng)
	output = "climate change script run successfully"

	return render( request, 'Slides.html', {'message': out.stdout} )
