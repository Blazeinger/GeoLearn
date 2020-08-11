from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
import requests
## from .models import Post
from google_images_download import google_images_download
import getpass
from pydrive.auth import GoogleAuth
from datetime import datetime

from .biodiversity.biodiversity_script_geolearn import find_animals_script
from .biodiversity.biodiversity_results_sorter import basic_image_finder
from .biodiversity.biodiversity_results_sorter import advanced_image_finder
from .biodiversity.enviro_log import enviro_logger

#from .climate_change.time_lapse import time_lapse
from subprocess import run,PIPE
import sys
import os
import threading
import csv
import time

from django.shortcuts import redirect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_DIR = BASE_DIR + '/python_scripts/'
BIO_DIR = SCRIPT_DIR + 'biodiversity/' 

logger = enviro_logger()

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

    # restart the log file 
    logger.restart()

    latitude = float( request.POST.get( 'Latitude' ) )
    longitude = float( request.POST.get( 'Longitude' ) )
    difficulty = request.POST.get( 'difficulty' )
    userEmail = request.POST.get( 'userEmail' )
    schoolName = request.POST.get( 'schoolName' )

    app_script_url = biodiversity_thread( longitude, latitude, difficulty, userEmail, schoolName )
    
    return redirect( app_script_url ) 
    
    
    
     

def biodiversity_thread( longitude, latitude, difficulty, userEmail, schoolName ):
    
    # Feed the lat and long to our find animals script
    # Now, we have the filename of the csv that contains the animal data
    csv_filename = None
    
    print( BASE_DIR )
    
    credentials_path = BASE_DIR + '/credentials.txt' 

    # Check for credentials 
    if os.path.isfile( credentials_path ):
    
        logger.log( "credentials exist" )
        
        # Check the time that the credentials were saved
        if 
        
            # if it was less than 30 minutes ago, return page that tells user that the website is being used. 
        
        # Otherwise, delete the credentials and redirect to credentials asking page
        
    # If there are no credentials
    else:
    
        # Save the time that the credential were saved
        save_credentials_time()
        
        # If there are no credentials, redirect to the page to ask for credentials
        ask_for_credentials()
        

    if difficulty == "beginner":
        
        logger.log( "beginner slideshow selected" )
        
        csv_filename = find_animals_script( latitude, longitude, "slideInfo_BioBasic" )
        
        #print( csv_filename )

        # Now, filter the animals to find which pictures we need to find
        basic_image_finder( True, "animal_images", csv_filename )
        
        # Delete the credentials for the user
        os.remove( BASE_DIR + '/credentials.txt' )
        
        app_script_url = "https://script.google.com/macros/s/AKfycbyKIAeXKYtMA4pdbBwpVWvZ_EqcElhQX9tJml9Xjbha_KhYMlw/exec?"
        app_script_url += "userEmail=" + userEmail
        app_script_url += "&schoolName=" + schoolName 
        
        logger.log( "going to " + app_script_url )
        #app_script_url = "https://script.google.com/macros/s/AKfycbwiCl5ILpsHtKbr6sK3fupy575qN2GAr1MsPp6EI4c/dev?userEmail="
        #app_script_url += userEmail + "&schoolName="
        #app_script_url += schoolName
        
        return app_script_url

    elif difficulty == "advanced":
    
        logger.log( "advanced slideshow selected" )
        
        csv_filename = find_animals_script( latitude, longitude, 'slideInfo_BioAdv' )

        advanced_image_finder( True, "animal_images", csv_filename )
        
        app_script_url = "https://script.google.com/macros/s/AKfycbx0Kd8n0uDVH0WIJ1PUiDRjK958hZbXrtXMUVJ7j74g/dev?userEmail="
        app_script_url += userEmail + "&schoolName="
        app_script_url += schoolName
        
        return app_script_url
        
        
        
        
        
def ask_for_credentials():

    logger.log( 'Asking user for credentials' )
    
    client_secrets_path = BASE_DIR + "/client_secrets.json" 
    
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_path
        
    # Create google account authentication objects
    gauth = GoogleAuth()
    return gauth.GetAuthUrl()
    
    
def save_credentials_time():

    with open( BASE_DIR + '/save_credentials_time.txt', mode='w', encoding='utf8' ) as text_file:
    
        now = datetime.now()
        
        text_file.write( now.strftime( '%d/%m/%Y %H:%M:%S' ) )
        
        
def check_save_time():
    
    with open( BASE_DIR + '/save_credentials_time.txt', mode='r', encoding='utf8' ) as text_file:
    
        time = text_file.read()
        
        
        

#def delete_credentials():
    






