# pip3 install selenium
# sudo apt-get install firefox-geckodriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time

from google_images_download import google_images_download

from bs4 import BeautifulSoup

# pip3 install Pillow
from PIL import Image

# These should just be from Python
import io
import requests
import urllib.request
from urllib.request import urlopen
import shutil
from shutil import copyfile
import os
import time
import csv
import re
import threading

try:
    from enviro_log import enviro_logger
except:
    from .enviro_log import enviro_logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
basest_dir = BASE_DIR.replace( "/python_scripts", "" )
SLIDES_DIR = basest_dir + "/slideshows/"
DEFAULT_IMAGE = SLIDES_DIR + "templates/default.jpg"

logger = enviro_logger()

BINOMIAL = 2
TITLE = 0
WIKIPEDIA_IMAGE_TO_AVOID = ['']

def main():    
    
    images_scraper( "chosen_mammals_info.csv" )
    
    

def wikipedia_download_image( target_image, images_dir ):
    
    ### Get a response from the wikipedia link
    # Check the whole name first 
    image_search_url = 'https://en.wikipedia.org/wiki/{search_query}'.format( search_query = correct_for_query_spaces( target_image ))
    
    #print( image_search_url )
    
    page_found = False
    
    # Loop thought different wikipedia searches to see if the page exists 
    while not page_found:
        
        # Create the response for the search 
        response = requests.get( image_search_url )
    
        ### Create the beautiful soup object
        soup = BeautifulSoup( response.text, 'html.parser' )
    
        ### Find the image   
        # Find the a tag elements with the class 'image' 
        images_class = soup.find_all( 'a', {'class': 'image'} )
        
        # Check if the page exists 
        if not images_class[0].find( 'img' ).get( 'alt' ) == 'Wiktionary-logo-v2.svg':
            page_found = True
            
        else:
            # Load a wiki page with only the first part of the binomial 
            image_search_url = 'https://en.wikipedia.org/wiki/{search_query}'.format( search_query = target_image.split()[0] )
    
    #print( image_parent )
    
    # Loop through the image class to find the image we want 
    index = 0
    image_not_found = True
    image_info = []
    
    while image_not_found:
        image_elements = images_class[index].find( 'img' )
        index += 1
        #print( image_elements )
        
        if not image_elements.get( 'alt' ) in WIKIPEDIA_IMAGE_TO_AVOID:
            image_not_found = False
            
            
    
    # Find its child that contains the image 
    print( 'getting elements' )
    image_info.append( 'https:' + str( image_elements.get( 'src' )))
    
    # Get its source 
    index = 0
    
    for image_url in image_info:
    
        #print( image_url )
        
        #try:
            #image = requests.get( image_url )
             
        return wikipedia_scrape( image_url, index, images_dir )
            #print( 'succeeded' )
            
        #except:
            #print( 'failed' )
        
        index += 1
        
    
def wikipedia_scrape( target_image_url, num, images_dir ):
    
    ### Rename the image locally
    
    image_file = io.BytesIO( requests.get( target_image_url ).content )
    
    image = Image.open( image_file ).convert( 'RGB' )
    
    image_name = 'most_recent_animal'
    
    image_path = images_dir + image_name + '.jpg' 
    
    image.save( image_path, 'JPEG', quality = 85 )
    
    return image_path
    
    
    

def use_image_not_found( image_title, images_dir ):
    
    copy_path = images_dir + image_title
    
    # Create a copy of the default image and name it the image title 
    copyfile( DEFAULT_IMAGE, copy_path )
    
    return copy_path
    
    
    


def images_scraper( chosen_csv, target_dir ):

    # Open the file 
    logger.log( "opening chosen mammals file" )

    images_dir = target_dir

    if not os.path.exists( images_dir ):
        os.mkdir( images_dir )
    
    # Loop through each animal 
    with open( chosen_csv, encoding='utf8' ) as csv_file:
    
        animal_reader = csv.reader( csv_file, delimiter = ',' )
        
        for animal in animal_reader:
    
    # Get the image of the animal 
            logger.log( 'downloading ' + animal[BINOMIAL] )
            
            # Try finding an image of the animal 
            try:
            
                image_path = wikipedia_download_image( animal[BINOMIAL], images_dir )
                print( animal[BINOMIAL] )
                print( animal[TITLE] ) 
                
                # Save the image as its title
                rename_valid_image( images_dir, image_path, animal[TITLE]  )               
                
            # If that all fails, use a default image
            except:
            
                print( "no image found" )
                # Create a copy of the default image and rename it 
                image_name = use_image_not_found( animal[BINOMIAL], images_dir )
                
                # Rename the image as its title
                os.rename( images_dir + animal[BINOMIAL], images_dir + animal[TITLE] + '.jpg' )
            
            
    
    
            




def find_animal_image( search_query, downloader ):
    
    # Create the arguments
    arguments = { "keywords": search_query,
                  "limit": 1,
                  "print_urls": True,
                  "format": 'jpg',
                  'output_directory': basest_dir,
                  'image_directory': 'animal_images',
                  'no_numbering': '-nn' }
    
    # download the arguments
    image_json = downloader.download( arguments )

    image_path = image_json[0][search_query][0]
    
    # return the path of the image
    return image_path
    





def rename_valid_image( images_dir, image_path, new_name ):

    # Run the cmd command to rename the image to the desired image
    os.rename( image_path, images_dir + new_name + ".jpg" )

    print( images_dir + new_name + '.jpg' )











'''

def old_images_scraper( dir_name=None, image_list=None, image_names=None ):

    # Make sure that the directory we create and save to is a valid name
    # Make sure what we name the image is a valid name
    directory_name = dir_name

    logger.log( "image scraping start" )
    
    if directory_name == None:
        directory_name = animal_search
        
    # Create our google image search url template 
    search_url = "https://www.google.co.in/search?q={search_query}&source=lnms&tbm=isch"

    try:
    
        # Connect our python script to our firefox browser
        driver = initialize_webdriver()

        #driver.set_page_load_timeout(300)

        if image_list != None and image_names != None:

            # Create a list of the image names that were found successfully
            successful_list = []

            index = 0

            # Loop thorugh the image list
            for image in image_list:

                logger.log( image[ 1 ][1] )
                
                # Change any spaces in the search query into pluses
                image_search = correct_for_query_spaces( image[ 1 ][1] )
        
                # Have our webdriver connect to our crafted url
                # The url replaces the "search query" with our actual search query
                driver.get( search_url.format( search_query = image_search ))
                
                time.sleep( 1 )
        
                # Check that the connection to the website was successful 
                assert "Google" in driver.title
                assert "No results found." not in driver.page_source
                
                successful_list.append( retrieve_image( image[ 1 ][1], driver, directory_name, image_names[ index ] ))

                index += 1

            driver.close()

            return successful_list
        
    except:
        logger.log( "images scraper crash" )
        driver.close()



def single_image_scraper( animal_name, image_name=None, dir_name=None, driver=None ):

    #try:
        # Make sure that the directory we create and save to is a valid name
        # Make sure what we name the image is a valid name
        directory_name = dir_name
        self_initialized_driver = False

        logger.log( "image scraping start" )
        
        if animal_name == None:
            return False
            
        if directory_name == None:
            directory_name = 'animal_images'
            
        # Please insert a webdriver. Using this method is insanely slow
        if driver == None:
            self_initialized_driver = True 
            driver = initialize_webdriver()
            
        if image_name == None: 
            image_name = animal_name
            
        logger.log( "all objects for downloading created" )
            
        # Change any spaces in the search query into pluses
        image_search = correct_for_query_spaces( animal_name )
        
        # Create our google image search url template 
        search_url = "https://www.google.co.in/search?q={search_query}&source=lnms&tbm=isch"
        
        # Have our webdriver connect to our crafted url
        # The url replaces the "search query" with our actual search query
        driver.get( search_url.format( search_query = image_search ))
        
        # Check that the connection to the website was successful 
        assert "Google" in driver.title
        assert "No results found." not in driver.page_source
                
        logger.log( "retrieving image" )
        
        retrieve_image( image_search, driver, directory_name, image_name )
        
        if self_initialized_driver:
            driver.close()
            
    #except:
        #driver.close()
     #   logger.log( "---> single image scraper crash" )
        
'''






def initialize_webdriver():
    #import tempfile

    #profile = tempfile.mkdtemp( ".selenium" )

    # Prevent the actual browser from opening
    options = webdriver.FirefoxOptions()
    options.binary_location = '/usr/bin/firefox'
    options.add_argument( 'headless' )
    #options.headless = e
    #options.add_argument( '--no-sandbox' )
    options.add_argument( '--mute-audio' )

    #display = Display(visible=0, size=(800, 600))
    #display.start()

    logger.log( 'connecting to webdriver' )
    
    successful_connection = False
    attempts = 0
    
    while not successful_connection:
    
        try:
            time.sleep( 10 )
            logger.log( "waiting 10 seconds to test connection" )
            
            # Connect our python script to our firefox browser
            driver = webdriver.Firefox( options=options, log_path=basest_dir + '/geckodriver.log', executable_path='/usr/bin/geckodriver' )
            
            logger.log( "successful webdriver connection" )
            successful_connection = True 
            return driver
            
        except:
        
            assert attempts < 3
            attempts += 1
            logger.log( "attempts to connect webdriver: " + str( attempts ) )

    display.stop()


def correct_for_query_spaces( search_query ):
    temp_query = search_query.split()
    return '_'.join( temp_query )
    
    
    
    
    

def retrieve_image( search_query, webdriver, dir_name, img_name ):

    try:

        logger.log( "image_scraping function start" ) 
        image_name = '' 
        
        # Variable that holds the number of images to fetch 
        number_of_images_to_fetch = 1
        index = 0

        # Scroll down the webpage to load more images
        scroll_down( webdriver )

        time.sleep( 5 )

        # Save all of the html image elements from our google search
        # 'rg_i' is the class name that the images have 
        image_elements = webdriver.find_elements_by_class_name( 'rg_i' )
        
        target_dir = basest_dir + "/" + dir_name

        # Check if the directory that we want to put our iamges in already exists
        if not os.path.exists( target_dir ):
        
           # If not, make that directory 
            os.mkdir( target_dir )


        found_image_count = 0
        attempt_count = 0
        logger.log( "begin finding images" )
        for element in image_elements:

            
            attempt_count += 1 
            
            try:

                # Check if you've downloaded all the images you want
                if found_image_count == number_of_images_to_fetch:
                    break

                # Click on the image you want to download 
                element.click()

                # Give the browser some time to catch up 
                time.sleep( 2 )        

                # After clicking on the image, get the larger version 
                found_image = webdriver.find_element_by_class_name( 'n3VNCb' )

                # find the source of the image, it's url 
                image_url = found_image.get_attribute( 'src' )

                logger.log( "attempt " + str( attempt_count ) + ": " + image_url[0:10]  )

                # Make sure that the image url is a valid source 
                if 'http' in image_url:

                    logger.log( "successful image found" )

                    # Download this image as a BytesIO object 
                    image_file = io.BytesIO( requests.get( image_url ).content )

                    # Convert our BytesIO object into an actual image
                    image = Image.open( image_file ).convert( 'RGB' )

                    # Create the the name of this image we're downloaded
                    image_name = img_name + '.jpg'

                    logger.log( image_name )

                    # Save the path that we want to save the image to
                    # The directory will be the same name as the search query 
                    image_path = target_dir + '/' + image_name

                    # Save the image 
                    image.save( image_path, 'JPEG', quality=85 )

                    found_image_count += 1

                # endif statement

            # end try block

            except:
                logger.log( "couldn't find enhanced images" )

            # end except block 
                  
        # End for loop  loop

        # close the web browser
        #webdriver.close()

        if attempt_count > 3:
            logger.log( "multiple attempts: " + search_query + "<=======" )

        else:
            logger.log( image_name )
        return image_name
        
    except:
        logger.log( "retrieve image crash" )
        webdriver.close()




def scroll_down( webdriver ):
    value = 0
    for i in range( 1 ):
        webdriver.execute_script( "scrollBy( 0, " + str(value) + ");" )
        value += 500
        time.sleep( .3 )


if __name__ == "__main__":
    main()
