from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
#from pyvirtualdisplay import Display

import time
try:
    from python_scripts.biodiversity.enviro_log import enviro_logger

except:
    from biodiversity.enviro_log import enviro_logger
from biodiversity.biodiversity_image_scraper import initialize_webdriver


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
<<<<<<< HEAD
#	try:
		driver = webdriver.Firefox( options=cmd_options, executable_path = '/usr/bin/geckodriver' )
		executor_url = driver.command_executor._url
		session_id = driver.session_id
		driver.get("http://www.google.com/")

=======
	try:
		#driver = webdriver.Firefox(options=cmd_options, executable_path = '/usr/bin/geckodriver' )
		driver = initialize_webdriver()
		driver.get("https://www.google.com/")
>>>>>>> 9128e2d8c6c530fa162ea636e49147a0fc74dcef
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
