import sys
import json
import pymysql.cursors
import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from optparse import OptionParser

#python3 alice.py -y 2016 -c 4
#python3 alice.py -y 2016 -c 4 -r
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

parser.set_defaults(
    year = "2016",
    cours_id = "1",
    register_switch = False
)

options, args = parser.parse_args()

register_switch = options.register_switch
year = options.year
cours = options.cours
save_file_name = "anime_" + year + "_C" + cours + ".csv"

get_date = datetime.now()
param = sys.argv

url = 'http://api.moemoe.tokyo/anime/v1/master/' + year + '/' + cours
result = requests.get(url)

master_list = json.loads(result.text)

meta_data_list = []

def parse_meta_data(bsObj):

    v = bsObj.find("meta", attrs={"name":"description"})
    description = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"name":"keywords"})
    keywords = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"name":"author"})
    author = v.get("content") if v else ""

    # --------- OGP ------------

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

    id = master['id']
    title = master['title']
    public_url = master['public_url']

    meta_data = {}

    meta_data['bases_id'] = str(id)
    meta_data['title'] = title
    meta_data['public_url'] = public_url
    meta_data['description'] = description
    meta_data['keywords'] = keywords
    meta_data['author'] = author
    meta_data['og_title'] = og_title
    meta_data['og_type'] = og_type
    meta_data['og_url'] = og_url
    meta_data['og_image'] = og_image
    meta_data['og_site_name'] = og_site_name
    meta_data['og_description'] = og_description

    meta_data_list.append(meta_data)

for master in master_list:

    print(master['title'] + " " + master['public_url'])

    html = requests.get(master['public_url'])

    try:
        bsObj = BeautifulSoup(html.text.encode(html.encoding), "html.parser")
        parse_meta_data(bsObj)
    except:
        # エンコードが認識できないサイトがあるので一度だけリトライする
        sys.stderr.write(master['public_url'])
        bsObj = BeautifulSoup(html.text.encode('utf8'), "html.parser")
        parse_meta_data(bsObj)


with open(save_file_name, 'wt') as fout:
    cout = csv.DictWriter(fout, ['bases_id', 'title', 'public_url', 'description','keywords',
                                 'author','og_title','og_type','og_url','og_image','og_site_name','og_description'])
    cout.writeheader()
    cout.writerows(meta_data_list)