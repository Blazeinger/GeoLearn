from django.urls import path
from . import views

'''
	The things in this list are urls that are accessible on the website
	Each url is associated with a different function in the 'views' python script 
	Each of these urls is given a name. These names are what are referenced in the html
	'''
	
urlpatterns = [ 
	path( '', views.index, name='index' ), 
	path( 'brother/', views.brother, name='brother' ), 
	path( 'Slides.html/', views.slides, name='slides' ), 
	path( 'index.html/', views.index, name='index' ),
	path( 'bio_output/', views.biodiversity_submit, name='bio_submit' ),
	path( 'climate_output/', views.climate_submit, name='climate_submit' ), 
] 
