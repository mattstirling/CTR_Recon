import ConfigParser
config = ConfigParser.ConfigParser()
config.read('config.ini')
print config.sections()
print config.get('filename','in_folder_CTR')

