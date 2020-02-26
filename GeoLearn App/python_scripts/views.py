from django.shortcuts import render
from django.http import HttpResponse

# Make sure you import the functions you want to use from other python scripts 
from .biodiversity.biodiversity_script_geolearn import find_animals_script
from .biodiversity.biodiversity_image_scraper import image_scraper
from .climate_change.time_lapse import time_lapse

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


# When this function is run, it will fun the 'find_animals_script' function 
# Then it renders the 'Slides.html' file, giving it the argument "biodiversity" 
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
	output = "biodiversity"
	find_animals_script( 35, -111 )
	return render( request, 'Slides.html', {'message': output} )
	
def climate_submit( request ):
	
	time_lapse()
	output = "cliamte change script ran successfully"
	return render( request, 'Slides.html', {'message': output} )
