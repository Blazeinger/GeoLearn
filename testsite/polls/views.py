from django.shortcuts import render
from django.http import HttpResponse
from .biodiversity.biodiversity_script_geolearn import find_animals_script

# Create your views here.
def index( request ):
	return render( request, 'index.html' )
	
def brother( request ):
	return HttpResponse( "hell yeah, brother" )
	
def slides( request ):
	return render( request, 'Slides.html' )

def biodiversity_submit( request ):
	
	find_animals_script( 35, -111 )
	output = "find animals script ran successfully" 
	return render( request, 'Slides.html', {'message': output} )
