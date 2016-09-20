import time
import sys
import json
import pymysql.cursors
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from optparse import OptionParser

#python3 alice.py -y 2016 -c 2
#python3 alice.py -y 2016 -c 2 -r
#python3 alice.py -y 2016 -c 2 -r -s anime2016C4.csv
parser = OptionParser()

parser.add_option(
    '-r', '--register_switch',
    action = 'store_true',
    dest = 'register_switch',
    help = 'DB register mode on'
)

parser.add_option(
    '-y', '--year',
    action = 'store',
    type = 'str',
    dest = 'year',
)

parser.add_option(
    '-c', '--cours',
    action = 'store',
    type = 'str',
    dest = 'cours',
)

parser.add_option(
    '-s', '--save-csv-filename',
    action = 'store',
    type = 'str',
    dest = 'save_filename',
)

parser.set_defaults(
    year = "2016",
    cours_id = "1",
    register_switch = False,
    save_file_name = "kamakiri.csv"
)

options, args = parser.parse_args()

register_switch = options.register_switch
year = options.year
cours = options.cours
save_file_name = options.save_file_name

get_date = datetime.now()
param = sys.argv

url = 'http://api.moemoe.tokyo/anime/v1/master/' + year + '/' + cours
result = requests.get(url)

master_list = json.loads(result.text)


print('og_title,og_type,og_url,og_image,og_site_name,og_description')

for master in master_list:

    #    print(master['title'] + " " + master['public_url'])

    html = requests.get(master['public_url'])

    bsObj = BeautifulSoup(html.text, "html.parser")

    v = bsObj.find("meta", attrs={"property":"og:title"})
    og_title = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property":"og:type"})
    og_type = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property":"og:url"})
    og_url = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property":"og:image"})
    og_image = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property":"og:site_name"})
    og_site_name = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property":"og:description"})
    og_description = v.get("content") if v else ""

    print(','.join([og_title, og_type, og_url, og_image, og_site_name, og_description]))
