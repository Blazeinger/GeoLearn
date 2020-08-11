from datetime import datetime

with open( 'save_credentials_time.txt', mode = 'w', encoding='utf8' ) as textfile: 
    now = datetime.now()
    now_string = now.strftime( '%d/%m/%Y %H:%M:%S' )
    
    print( now_string )
    textfile.write( now_string )
