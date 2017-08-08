import os
import sys

script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_path)

# csv_full_path = os.path.join(script_path, 'movies.csv')
#
# csv_output = ' -o ' + csv_full_path
# logging level
level = 'DEBUG'  # DEBUG INFO WARNING ERROR CRITICAL
logging_output = ' -L ' + level

cmd = 'scrapy crawl movies' + logging_output + '> movies.log'
os.system(cmd)
