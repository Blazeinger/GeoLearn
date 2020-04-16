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
	path( 'Slides.html/', views.slides, name='slides' ),
	path( 'index.html/', views.index, name='index' ),
	path( 'biodiversity.html/', views.bio, name='biodiversity' ),
	path( 'climate.html/', views.climate, name='climate' ),
	path( 'Spinner.html/', views.spinner, name='spinner' ),
	path( 'faq.html/', views.faq, name='faq' ),
	path( 'about.html/', views.about, name='about' ),
	path( 'team.html/', views.team, name='team' ),
	path( 'bio_output/', views.biodiversity_submit, name='bio_submit' ),
	url( r'bio_output', views.biodiversity_submit, name='bio_submit' ), 
	url(r'climate_output', views.climate_submit, name="climate_submit"),
	url( r'combined_output', views.biodiversity_climate_submit, name="combined_output" )
]
