from django.shortcuts import render
from django.http import HttpResponse
from .biodiversity.biodiversity_script_geolearn import find_animals_script
from .biodiversity.biodiversity_results_sorter import find_animal_images

#from .climate_change.time_lapse import time_lapse
from subprocess import run,PIPE
import sys
import os
from django.shortcuts import redirect

# Finds the absolute path to this directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

def bio_slides_page( request ):
	return render( request, 'biodiversity.html' )

def climate_slides_page( request ):
	return render( request, 'climate.html' )

def landuse_slides_page( request ):
	return render( request, 'land.html' )


def biodiversity_submit( request ):

        print( "i hate python" )

        # Fetch the longitude and latitude from the form on the slides page
        lat = float( request.POST.get( 'Latitude' ) )
        lng = float( request.POST.get( 'Longitude' ) )

        # Feed the lat and long to our find animals script
        # Now, we have the filename of the csv that contains the animal dat
        csv_filename = find_animals_script( lat, lng )

        # Now, filter the animals to find which pictures we need to find
        find_animal_images( csv_filename, True, "animal_images" )

        output = csv_filename
        return render( request, 'Slides.html', {'message': output} )

def climate_submit( request ):
	lat = request.POST.get('lat')
	lng = request.POST.get('long')

	timelapse_path = BASE_DIR + '/python_scripts/climate_change/time_lapse.py'

	#out = run([sys.executable,
	#'//mnt//c//Users//Samuel Prasse//Documents//GitHub//GeoLearn//GeoLearn App//GeoLearn-django_website//testsite//polls//climate_change//time_lapse.py', lat, lng], shell=False, stdout=PIPE)

	out = run([sys.executable, timelapse_path, lat, lng], shell=False, stdout=PIPE )

	#time_lapse(lat, lng)
	output = "climate change script run successfully"

	return render( request, 'Slides.html', {'message': out.stdout} )

def biodiversity_climate_submit( request ):

	# Float values of longitude and latitude
	# Fetch the longitude and latitude from the form on the slides page
	latitude = float( request.POST.get( 'Latitude' ) )
	longitude = float( request.POST.get( 'Longitude' ) )
	difficulty = request.POST.get( 'difficulty' )
	userEmail = request.POST.get( 'userEmail' )
	schoolName = request.POST.get( 'schoolName' )

	print(f"Diff: {difficulty}, Email: {userEmail}, School: {schoolName}")

	# Feed the lat and long to our find animals script
	# Now, we have the filename of the csv that contains the animal data
	csv_filename = find_animals_script( latitude, longitude )

	# Now, filter the animals to find which pictures we need to find
	find_animal_images( csv_filename, True, "animal_images" )
	#output = csv_filename
	#return render( request, 'Slides.html', {'message': output} )

	timelapse_path = BASE_DIR + '/python_scripts/climate_change/time_lapse.py'
	out = run([sys.executable, timelapse_path, str(latitude), str(longitude)], shell=False, stdout=PIPE )

	#time_lapse(lat, lng)
	output = "climate change script run successfully"
	
	if difficulty == "beginner":
	
		app_script_url = "https://script.google.com/macros/s/AKfycbwiCl5ILpsHt"
		app_script_url += "Kbr6sK3fupy575qN2GAr1MsPp6EI4c/dev?userEmail="
		app_script_url += userEmail + "&schoolName="
		app_script_url += schoolName
		
	return redirect( app_script_url )
