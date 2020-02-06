from django.urls import path
from . import views

urlpatterns = [ 
	# index is the name of the function in views.py
	path( '', views.index, name='index' ), 
	path( 'polls/', views.brother, name='brother' ), 
	path( 'Slides.html/', views.slides, name='slides' ), 
	path( 'index.html/', views.index, name='index' ),
] 
