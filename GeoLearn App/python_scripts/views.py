from django.shortcuts import render
from django.http import HttpResponse
from selenium import webdriver
## from .models import Post

if __name__ == "__main__":
    True

else:
    from .biodiversity.biodiversity_script_geolearn import find_animals_script
    from .biodiversity.biodiversity_image_scraper import images_scraper, single_image_scraper, initialize_webdriver
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
    logger = enviro_logger()
    logger.restart()

    # Float values of longitude and latitude
    # Fetch the longitude and latitude from the form on the slides page
    latitude = float( request.POST.get( 'Latitude' ) )
    longitude = float( request.POST.get( 'Longitude' ) )
    difficulty = request.POST.get( 'difficulty' )
    userEmail = request.POST.get( 'userEmail' )
    schoolName = request.POST.get( 'schoolName' )

    print(f"Diff: {difficulty}, Email: {userEmail}, School: {schoolName}")

    '''
    bio_thread = threading.Thread( target=biodiversity_thread, args=( longitude, latitude, difficulty, userEmail, schoolName, ) )
    bio_thread.start()

    return render( request, 'Spinner.html' )
    '''

    # Feed the lat and long to our find animals script
    # Now, we have the filename of the csv that contains the animal data
    csv_filename = None

    if difficulty == "beginner":
        
        
        csv_filename = find_animals_script( latitude, longitude, "slideInfo_Bio" )
        assert csv_filename != None

        # Now, filter the animals to find which pictures we need to find
        chosen_csv_name = basic_image_finder( True, "animal_images", csv_filename )
        
        driver = webdriver.Firefox()

        index = 0
        
        '''
        with open( chosen_csv_name, encoding="utf8" ) as csv_file:
            curr_reader = csv.reader( csv_file )

            for animal in curr_reader:
                single_image_scraper( animal[2], animal[0], "animal_images", webdriver )

                index += 1
        '''
        
        app_script_url = "https://script.google.com/macros/s/AKfycbwiCl5ILpsHt"
        app_script_url += "Kbr6sK3fupy575qN2GAr1MsPp6EI4c/dev?userEmail="
        app_script_url += userEmail + "&schoolName="
        app_script_url += schoolName
        
        activate_google_script_url( difficulty, userEmail, schoolName, driver )

                                      

    elif difficulty == "advanced":
    
        while csv_filename == None:
            csv_filename = find_animals_script( latitude, longitude, "slideInfo_BioAdv" )

        advanced_image_finder( True, "animal_images", csv_filename )

        '''
        #Insert app script url stuff here, Kaitlyn
        '''
		
    print( "redirected to slideshow creation url" )
    return render( request, 'Spinner.html' )
    



def biodiversity_thread( longitude, latitude, difficulty, userEmail, schoolName ):
    
    # Feed the lat and long to our find animals script
    # Now, we have the filename of the csv that contains the animal data
    csv_filename = None

    if difficulty == "beginner":
        
        '''
        csv_filename = find_animals_script( latitude, longitude, "slideInfo_Bio" )
        assert csv_filename != None

        # Now, filter the animals to find which pictures we need to find
        chosen_csv_name = basic_image_finder( True, "animal_images", csv_filename )
        '''
        driver = webdriver.Firefox()

        index = 0
        
        '''
        with open( chosen_csv_name, encoding="utf8" ) as csv_file:
            curr_reader = csv.reader( csv_file )

            for animal in curr_reader:
                single_image_scraper( animal[2], animal[0], "animal_images", webdriver )

                index += 1
        '''
        
        app_script_url = "https://script.google.com/macros/s/AKfycbwiCl5ILpsHt"
        app_script_url += "Kbr6sK3fupy575qN2GAr1MsPp6EI4c/dev?userEmail="
        app_script_url += userEmail + "&schoolName="
        app_script_url += schoolName
        
        activate_google_script_url( difficulty, userEmail, schoolName, driver )

                                      

    elif difficulty == "advanced":
    
        while csv_filename == None:
            csv_filename = find_animals_script( latitude, longitude, "slideInfo_BioAdv" )

        advanced_image_finder( True, "animal_images", csv_filename )

        '''
        #Insert app script url stuff here, Kaitlyn
        '''
		
    print( "redirected to slideshow creation url" )
    
    


def activate_google_script_url( difficulty, userEmail, schoolName, driver ):
    
    if difficulty == "beginner":
        
        app_script_url = "https://script.google.com/macros/s/AKfycbwiCl5ILpsHtKbr6sK3fupy575qN2GAr1MsPp6EI4c/dev?userEmail=" + userEmail + "&schoolName=" + schoolName
        
    elif difficulty == "advanced": 
    
        ''' Insert url here '''

    driver.get( app_script_url )
    
    on_signin_screen = False
    
    time.sleep( 5 )
    
    # Check if the url directs to a sign-in screen 
    #try:
    print( "finding sign-in screen" )
    page_title = driver.find_element_by_tag_name( "title" )
        
    print( "on sign-in screen" )
        
    if page_title.get_attribute( "innerHTML" ) == 'Google Drive: Sign-in':
        
        print( "totally was sign-in screen" )
        on_signin_screen = True
        
    #except:
    #    print( "wasn't sign-in screen" )
    
    # sign into the email 
    if on_signin_screen:
        
        # Fill in email
        
        ## find the login area 
        text_area = driver.find_element_by_id( 'identifierId' )
        
        ## click on it
        text_area.click()
        
        ## fill it in
        text_area.send_keys( "geolearnweb@gmail.com" )
        
        ## find the submit button 
        submit_button = driver.find_element_by_id( 'identifierNext' )
        
        ## click on the submit button 
        submit_button.click()
        
        time.sleep( 1 )
        
        # Fill in the password
        
        ## find the text area
        text_area = driver.find_element_by_name( 'password' )
        
        ## click on it
        text_area.clear() #click()
        
        ## fill it in
        text_area.send_keys( "Capstone2020" )
        
        ## find the submit button 
        submit_button = driver.find_element_by_id( 'passwordNext' )
        
        ## click on the submit button 
        submit_button.click()
        
        # Wait 2 minutes for the slideshow to be created
        
        ## Let the user know 
        print( "waiting 2.5 minutes for slideshow to be created" )
        
        ## wait
        for half_minute in range( 1, 6 ):
            time.sleep( 30 )
            elapsed_time = 30 * half_minute
            print( elapsed_time + " has passed" )
            
        print( "slideshow has been created" )
    driver.close()


if __name__ == "__main__":
    biodiversity_thread( -111, 35, "beginner", "joshusttenakhongva@gmail.com", "2:00 test" )



