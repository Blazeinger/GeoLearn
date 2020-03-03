# pip3 install selenium
# sudo apt-get install firefox-geckodriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import time

# pip3 install Pillow
from PIL import Image

# These should just be from Python
import io
import requests
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    while True:
        print( "type animal name: " )
        image_scraper( input(), "animal_images", "animals" )

def image_scraper( animal_search, dir_name=None, img_name=None ):

    # Make sure that the directory we create and save to is a valid name
    # Make sure what we name the image is a valid name
    directory_name = dir_name
    image_name = img_name
    
    if directory_name == None:
        directory_name = animal_search

    if image_name == None:
        image_name = animal_search
        
    # Create our google image search url template 
    search_url = "https://www.google.co.in/search?q={search_query}&source=lnms&tbm=isch"

    # Prevent the actual browser from opening
    options = Options()
    options.add_argument( '--headless' )
    
    # Connect our python script to our firefox browser
    driver = webdriver.Firefox( options=options )

    # Change any spaces in the search query into pluses
    image_search = correct_for_query_spaces( animal_search )

    # Have our webdriver connect to our crafted url
    # The url replaces the "search query" with our actual search query
    driver.get( search_url.format( search_query = image_search ))

    # Check that the connection to the website was successful 
    assert "Google" in driver.title
    assert "No results found." not in driver.page_source

    ''' Retreive the URLs for the images we're searching for '''
    return retrieve_image_urls( animal_search, driver, directory_name, image_name  )


def correct_for_query_spaces( search_query ):
    temp_query = search_query.split()
    return '+'.join( temp_query )

def retrieve_image_urls( search_query, webdriver, dir_name, img_name ):

    image_name = '' 

    # Variable that holds the number of images to fetch 
    number_of_images_to_fetch = 1
    index = 0

    # Scroll down the webpage to load more images
    #scroll_down( webdriver )

    # Save all of the html image elements from our google search
    # 'rg_i' is the class name that the images have 
    image_elements = webdriver.find_elements_by_class_name( 'rg_i' )

    # Check if the directory that we want to put our iamges in already exists
    if not os.path.exists( BASE_DIR + "/biodiversity/" + dir_name ):

       # If not, make that directory 
        os.mkdir( BASE_DIR + "/biodiversity/" + dir_name )

    ''' 
    Loop through the image elements gathered and translate them to 
    URLs and then to actual images 
    '''
    found_image_count = 0
    attempt_count = 0
    
    for element in image_elements:

        
        attempt_count += 1 

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

        print( "attempt " + str( attempt_count ) + ": " + image_url[0:10]  )

        # Make sure that the image url is a valid source 
        if 'http' in image_url:

            print( "successful image found" )

            # Download this image as a BytesIO object 
            image_file = io.BytesIO( requests.get( image_url ).content )

            # Convert our BytesIO object into an actual image
            image = Image.open( image_file ).convert( 'RGB' )

            # Create the the name of this image we're downloaded
            image_name = img_name + '.jpg'

            print( image_name )

            # Save the path that we want to save the image to
            # The directory will be the same name as the search query 
            image_path = BASE_DIR + "/biodiversity/" + dir_name + '/' + image_name

            # Save the image 
            image.save( image_path, 'JPEG', quality=85 )

            found_image_count += 1

        
    '''
    for index in range( number_of_images_to_fetch ):

        image_elem = image_elements[ index ]

        image_elem.click()

        time.sleep( 1 )

        actual_image = webdriver.find_element_by_class_name( 'n3VNCb' )
        
        # Find the url of the image that we want tn download 
        image_url = actual_image.get_attribute( 'src' )
    '''
        


    # close the web browser
    webdriver.close()

    print( image_name )
    return image_name


'''
Method that scrolls down the webpage to load more images
'''
def scroll_down( webdriver ):
    value = 0
    for i in range( 1 ):
        webdriver.execute_script( "scrollBy( 0, " + str(value) + ");" )
        value += 500
        time.sleep( .3 )


if __name__ == "__main__":
    main()