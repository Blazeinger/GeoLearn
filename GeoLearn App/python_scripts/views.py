from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
import requests
## from .models import Post
from google_images_download import google_images_download
import getpass
from pydrive.auth import GoogleAuth
from datetime import datetime, timedelta

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
import math

from django.shortcuts import redirect

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_DIR = BASE_DIR + '/python_scripts/'
BIO_DIR = SCRIPT_DIR + 'biodiversity/' 
CRED_TIME_PATH = BASE_DIR + '/save_credentials_time.txt'
CRED_PATH = BASE_DIR + '/credentials.txt' 
CRED_TIMEOUT = timedelta( minutes = 30 )

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
	
def auth_redirect( request ):
    return redirect( ask_for_credentials() )

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
    authCode = request.POST.get( 'authCode' )
    
    # First, check if there is an authcode input
    try:
        input_auth_code( authCode )
    
    except:
        return redirect( ask_for_credentials() )

    # Check for credentials 
    if os.path.isfile( CRED_PATH ):
    
        logger.log( "credentials exist" )
        
        # Check the time that the credentials were saved
        if check_cred_timeout(): 
        
            # If it did timeout, delete the credentials and redirect to credentials asking page
            return redirect( ask_for_credentials() )
            
        '''
        else:
        
            # Otherwise, it was less than 30 minutes ago, return page that tells user that the website is being used. 
            time_remaining = CRED_TIMEOUT - get_cred_time_remaining() 
            minutes_remaining = math.ceil( time_remaining.seconds / 60 )
                
            response_string = "The website it currently in use. It will be available in {} minutes".format( minutes_remaining )
            
            return HttpResponse( response_string )
            
        '''
        
    # If there are no credentials or authcode
    else:
    
        # Save the time that the credential were saved
        save_credentials_time()
        
        # If there are no credentials, redirect to the page to ask for credentials
        return redirect( ask_for_credentials() )

    # If the credentials are all setup within the timeout time, run the program normally
    app_script_url = biodiversity_thread( longitude, latitude, difficulty, userEmail, schoolName )
    
    return redirect( app_script_url ) 
    
    
    
     

def biodiversity_thread( longitude, latitude, difficulty, userEmail, schoolName ):
    
    # Feed the lat and long to our find animals script
    # Now, we have the filename of the csv that contains the animal data
    csv_filename = None
    
    print( BASE_DIR )        

    if difficulty == "beginner":
        
        logger.log( "beginner slideshow selected" )
        
        csv_filename = find_animals_script( latitude, longitude, "slideInfo_BioBasic" )

        # Now, filter the animals to find which pictures we need to find
        basic_image_finder( True, "animal_images", csv_filename )
        
<<<<<<< HEAD
        # Create the URL for the Google App Script to contain the parameters
        app_script_url = "https://script.google.com/macros/s/AKfycbyKIAeXKYtMA4pdbBwpVWvZ_EqcElhQX9tJml9Xjbha_KhYMlw/exec?"
        app_script_url += "userEmail=" + userEmail
        app_script_url += "&schoolName=" + schoolName 
        
        # Let the logger know that the url has been created, and the program is being redirected there. 
        logger.log( "going to app script url" )
=======
        logger.log( "trying to webdrive for google script url" )
        driver = initialize_webdriver()
        logger.log( "successfully web drove" )
>>>>>>> 760ae629f5368ca846b7e7755c0cad50f3d0a157
        
        # Delete the user's Google Drive credentials
        delete_credentials()
        
        # Return the url to the creation script
        return app_script_url


    # Check if the slideshow selected is an advanced slideshow
    elif difficulty == "advanced":
    
        logger.log( "advanced slideshow selected" )
        
        # Find the animals in that area
        csv_filename = find_animals_script( latitude, longitude, 'slideInfo_BioAdv' )

        # Find the images for the slideshow and upload them to the user's Google Drive
        advanced_image_finder( True, "animal_images", csv_filename )
        
        # Craft the creation script url with the parameters
        app_script_url = "https://script.google.com/macros/s/AKfycbxDf3BPsgdZK_mn-2v5vc6TljEb8rtjpM0Qptb8wcw4VIaeB8GV/exec?"
        app_script_url += 'userEmail=' + userEmail
        app_script_url += '&schoolName=' + schoolName 
        
        # Let the logger know that the url has been created, and the program is being redirected there. 
        logger.log( "going to app script url" )
        
        # Delete the user's credentials 
        delete_credentials()
        
        # Redirect the user to the app creation script url 
        return app_script_url
        
        
        
        
        
def ask_for_credentials():

    logger.log( 'Asking user for credentials' )
    
    client_secrets_path = BASE_DIR + "/client_secrets.json" 
    
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_path
        
    # Create google account authentication objects
    gauth = GoogleAuth()
    return gauth.GetAuthUrl()
    
def input_auth_code( code ):
    logger.log( 'checking auth code' )
    
    client_secrets_path = BASE_DIR + "/client_secrets.json" 
    
    GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_path
        
    # Create google account authentication objects
    gauth = GoogleAuth()
    
    # Input the auth code
    gauth.Auth( code )
    
    # Save the credentials if they're valid
    gauth.SaveCredentialsFile( CRED_PATH )
    
    save_credentials_time()
    
    logger.log( 'credentials saved and validated' )
    
def save_credentials_time():

    with open( CRED_TIME_PATH, mode='w', encoding='utf8' ) as text_file:
    
        now = datetime.now()
        
        text_file.write( now.strftime( '%d/%m/%Y %H:%M:%S' ) )
        
        
def get_cred_time_remaining():
    
    with open( CRED_TIME_PATH, mode='r', encoding='utf8' ) as text_file:
    
        # Get the time that the credentials were saved and convert to a time datatype
        read_datetime = text_file.read()
        
        # Convert it to a datetime object 
        date, time = read_datetime.split()
        
        date = date.split( '/' )
        time = time.split( ':' )
        
        for index in range( 0, 3 ):
            date[index] = int( date[index] )
            time[index] = int( time[index] )
            
        read_datetime = datetime( date[2], date[1], date[0], time[0], time[1], time[2] )
       
        return datetime.now() - read_datetime
       
def check_cred_timeout():

    return get_cred_time_remaining() > CRED_TIMEOUT

def delete_credentials():
    if os.path.exists( CRED_PATH ):
        os.remove( CRED_PATH )
        logger.log( 'credentials deleted' )
        
    else:
        logger.log( 'credentials not deleted' )






