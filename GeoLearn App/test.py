from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import time
from biodiversity.enviro_log import enviro_logger
from biodiversity.biodiversity_image_scraper import initialize_webdriver


logger = enviro_logger()
logger.restart()

cmd_options = FirefoxOptions()
cmd_options.headless = True


logger.log( "sleeping 10 seconds" )
time.sleep( 10 )

attempts = 3
while( attempts > 0 ):
	try:
		#driver = webdriver.Firefox(options=cmd_options, executable_path = '/usr/bin/geckodriver' )
		driver = initialize_webdriver()
		driver.get("https://www.google.com/")
		logger.log (driver.title)

		driver.close()
		attempts = 0
	except: 
		logger.log( "failed again" )
		attempts -= 1

logger.log( "went all the way through" )

