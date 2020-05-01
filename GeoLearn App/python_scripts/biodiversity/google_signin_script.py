from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import io
import requests


def main():

    # Create a web driver
    driver = webdriver.Firefox()

    # Have it connect to the google url
    driver.get( "google.com" )
    




if __name__ == "__main__":
    main()
