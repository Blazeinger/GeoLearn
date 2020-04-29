from django.shortcuts import render
from django.http import HttpResponse
## from .models import Post
from .biodiversity.biodiversity_script_geolearn import find_animals_script
from .biodiversity.biodiversity_image_scraper import images_scraper, single_image_scraper, initialize_webdriver
from .biodiversity.biodiversity_results_sorter import basic_image_finder
from .biodiversity.biodiversity_results_sorter import advanced_image_finder

#from .climate_change.time_lapse import time_lapse
from subprocess import run,PIPE
import sys
import os
import threading
import csv
import time

from django.shortcuts import redirect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
'''
Views are the python function that are associated with different urls.
When you go to a URL in the 'urls.py', it will run the function in this script
In the urls script, you can see that the path '' is associated with the index
function just below. When you go to localhost with no extension, it will run
the index function.
'''
def index( request ):
	# render, the way I'm using it, just runs an html file.
	# It may do other things that I don't know, but that's what it's doing here
	'''
	context = {
		'posts': Post.objects.order_by('-date')
		if request.user.is_authenticated else[]
	}
	'''
	return render( request, 'index.html' )

def slides( request ):
	return render( request, 'Slides.html' )
	
def team( request ):
	return render( request, 'team.html' )
	
def bio( request ):
	return render( request, 'biodiversity.html' )
	
def climate( request ):
	return render( request, 'climate.html' )

def spinner( request ):
	return render( request, 'Spinner.html' )
	
def faq( request ):
	return render( request, 'faq.html' )
	
def about( request ):
	return render( request, 'about.html' )
	
def disease( request ):
	return render( request, 'disease.html' )







def biodiversity_submit( request ):
        
	# Fetch the longitude and latitude from the form on the slides page 
	lat = float( request.POST.get( 'lat' ) )
	lng = float( request.POST.get( 'long' ) )
	
	# Feed the lat and long to our find animals script 
	# Now, we have the filename of the csv that contains the animal data 
	csv_filename = find_animals_script( lat, lng )
	
	# Now, filter the animals to find which pictures we need to find 
	find_animal_images( csv_filename, True, "animal_images" )
	
	output = csv_filename 
	return render( request, 'Slides.html', {'message': output} )







def climate_submit( request ):
	lat = request.POST.get('lat') 
	lng = request.POST.get('long') 

	out = run([sys.executable,
	'//mnt//c//Users//Samuel Prasse//Documents//GitHub//GeoLearn//GeoLearn App//GeoLearn-django_website//testsite//polls//climate_change//time_lapse.py', lat, lng], shell=False, stdout=PIPE)

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
    
    while csv_filename == None:
        time.sleep(1)

    if difficulty == "beginner":

        # Now, filter the animals to find which pictures we need to find
        chosen_csv_name = basic_image_finder( csv_filename, True, "animal_images" )

        webdriver = initialize_webdriver()

        index = 0
        
        with open( chosen_csv_name, encoding="utf8" ) as csv_file:
            curr_reader = csv.reader( csv_file )

            for animal in curr_reader:
                single_image_scraper( animal[2], animal[0], "animal_images", webdriver )

                index += 1
                
                '''
                if index == 10:
                    output_thread = threading.Thread( target=show_user_progress )
                    
                    output_thread.start()
                    
                '''
        
        app_script_url = "https://script.google.com/macros/s/AKfycbwiCl5ILpsHt"
        app_script_url += "Kbr6sK3fupy575qN2GAr1MsPp6EI4c/dev?userEmail="
        app_script_url += userEmail + "&schoolName="
        app_script_url += schoolName



                                      

    elif difficulty == "advanced":

        advanced_image_finder( csv_filename, True, "animal_images" )

        '''
        #Insert app script url stuff here, Kaitlyn
        '''
		
    print( "redirected to slideshow creation url" )

    return redirect( app_script_url )
    
    


def show_user_progress( output ):
    return render( request, 'Spinner.html' )
