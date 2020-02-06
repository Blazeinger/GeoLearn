from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index( request ):
	return render( request, 'index.html' )
	
def brother( request ):
	return HttpResponse( "hell yeah, brother" )
	
def slides( request ):
	return render( request, 'Slides.html' )
