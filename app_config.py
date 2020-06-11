
# General Config
debug_mode = True

# Web Config
host_name = '0.0.0.0'
port = 5000
api_url = '/api/articles/bbc'


# Database Access Config
#mongodb+srv://bouchra:08051998@cluster0-5drqg.mongodb.net/test?retryWrites=true&w=majority
#db_conn_string = 'mongodb+srv://isentia:isentia@cluster0-aoq9j.mongodb.net/admin'
db_conn_string = 'mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass%20Community&ssl=false'
db_name = 'scraped_news2'
collection_name = 'bbc_articles'


# News Scraping Config
base_url = 'http://www.bbc.com/'
removing_strings = ['Media playback is unsupported on your device ']
csv_file_name = 'news_scraped.csv'