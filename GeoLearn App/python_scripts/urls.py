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
	path( '', views.index, name='index' ),
	path( 'brother/', views.brother, name='brother' ),
	path( 'Slides.html/', views.slides, name='slides' ),
	path( 'index.html/', views.index, name='index' ),
	path( 'bio_output/', views.biodiversity_submit, name='bio_submit' ),
	path( 'biodiversity.html', views.bio_slides_page, name='bio_slides_page' ),
	path( 'climate.html', views.climate_slides_page, name='climate_slides_page' ),
	path( 'land.html', views.landuse_slides_page, name='landuse_slides_page' ),
	url( r'bio_output', views.biodiversity_submit, name='bio_submit' ),
	url(r'climate_output', views.climate_submit, name="climate_submit"),
    url( r'combined_output', views.biodiversity_climate_submit, name='combined_submit' )
]
