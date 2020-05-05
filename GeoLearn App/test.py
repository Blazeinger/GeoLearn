from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
#from pyvirtualdisplay import Display

import time
from python_scripts.biodiversity.enviro_log import enviro_logger


logger = enviro_logger()
logger.restart()

#pyvirtualdisplay shit
#display = Display(visible=0, size=(800, 600))
#display.start()

cmd_options = webdriver.FirefoxOptions()
cmd_options.binary_location = '/usr/bin/firefox'
cmd_options.add_argument( 'headless' )
#cmd_options.add_argument( '--no-sandbox' )

logger.log( "sleeping 5 seconds" )
time.sleep( 5 )

attempts = 3
while( attempts > 0 ):
#	try:
		driver = webdriver.Firefox( options=cmd_options, executable_path = '/usr/bin/geckodriver' )
		executor_url = driver.command_executor._url
		session_id = driver.session_id
		driver.get("http://www.google.com/")

		logger.log (driver.title)
		logger.log(executor_url)
		logger.log( session_id )
		logger.log( driver.current_url )

		driver.close()
		attempts = 0
#	except: 
		logger.log( "failed again" )
		attempts -= 1

logger.log( "went all the way through" )
display.stop()
