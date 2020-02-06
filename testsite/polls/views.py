from django.shortcuts import render
from django.http import HttpResponse
#from biodiversity import test

# Create your views here.
def index( request ):
	return render( request, 'index.html' )
	
def brother( request ):
	return HttpResponse( "hell yeah, brother" )
	
def slides( request ):
	return render( request, 'Slides.html' )

def biodiversity_submit( request ):
	output = 'hello world!!!' 
	print( 'hello world' ) 
	return render( request, 'Slides.html', {'message': output} )
