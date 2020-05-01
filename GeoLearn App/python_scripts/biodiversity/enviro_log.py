
class enviro_logger():
    
    def __init__( self ):
        
        self.text_file_name = "log_output.txt" 
        
    def log( self, string ):
        print( str( string ) )
        with open( self.text_file_name, mode='a', encoding='utf8' ) as csv_file:
            csv_file.write( str( string ) + "\n" )
