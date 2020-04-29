from django.urls import path
from django.conf.urls import url
from . import views

'''
The things in this list are urls that are accessible on the website
Each url is associated with a different function in the 'views' python script
Each of these urls is given a name. These names are what are referenced in the html
'''

urlpatterns = [
	# index is the name of the function in views.py
	path( 'front-end/', views.index, name='index' ),
	path( 'front-end/brother/', views.brother, name='brother' ),
	path( 'front-end/Slides.html/', views.slides, name='slides' ),
	path( 'front-end/index.html/', views.index, name='index' ),
	path( 'front-end/biodiversity.html/', views.bio, name='biodiversity' ),
	path( 'front-end/climate.html/', views.climate, name='climate' ),
	path( 'front-end/land.html/', views.land, name='land' ),
	#path( 'front-end/bio_output/', views.biodiversity_submit, name='bio_submit' ),
	url( r'bio_output', views.biodiversity_submit, name='bio_submit' ), 
	url(r'climate_output', views.climate_submit, name="climate_submit")
]
