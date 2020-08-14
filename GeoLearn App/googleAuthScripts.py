from datetime import datetime, timedelta
import math

CRED_TIMEOUT = timedelta( minutes = 30 ) 

with open( 'save_credentials_time.txt', mode = 'w', encoding='utf8' ) as textfile: 
    now = datetime( 2020, 8, 12, 12, 30, 0 )
    now_string = now.strftime( '%d/%m/%Y %H:%M:%S' )
    
    print( now_string )
    textfile.write( now_string )

    now_date, now_time = now_string.split()
    
    now_date = now_date.split( '/' )
    now_time = now_time.split( ':' )
    
    for index in range( 0, 3 ):
        now_date[ index ] = int( now_date[ index ] )
        now_time[ index ] = int( now_time[ index ] )
    
    print( now_date )
    print( now_time )
    
    date_object = datetime( now_date[2], now_date[1], now_date[0], now_time[0], now_time[1], now_time[2] )
    
    print( 'object: ', end='' )
    print( date_object )
    
    now2 = datetime.now()
    
    
    print( 'now2 is after now1: ' )
    time_difference = now2 - date_object
    
    print( math.ceil( time_difference.seconds / 60)  )
    print( time_difference > CRED_TIMEOUT )
    
