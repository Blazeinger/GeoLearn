# biodiversity urls script

from django.urls import path
import test

urlpatterns = [ 
	# index is the name of the function in views.py
	path( '', test, name='test' )
] 
