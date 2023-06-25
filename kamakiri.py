import sys
import traceback
import json
import pymysql.cursors
from urllib.request import urlretrieve
import requests
import os.path
import os
import csv
import re
from datetime import datetime
from bs4 import BeautifulSoup
from optparse import OptionParser

#python3 alice.py -y 2016 -c 4
#python3 alice.py -y 2016 -c 4 -r

SAVE_OGIMAGE_PATH = "./og_image/"

parser = OptionParser()

parser.add_option(
    '-r', '--register_flag',
    action='store_true',
    dest='register_flag',
    help='DB register mode on'
)

parser.add_option(
    '-s', '--save_image_flag',
    action='store_true',
    dest='save_image_flag',
    help='save image flag'
)

parser.add_option(
    '-y', '--year',
    action='store',
    type='str',
    dest='year',
)

parser.add_option(
    '-c', '--cours',
    action='store',
    type='str',
    dest='cours',
)

parser.set_defaults(
    year="2016",
    cours_id="1",
    register_switch=False,
    save_image_flag=False
)

options, args = parser.parse_args()

register_flag = options.register_flag
save_image_flag = options.save_image_flag
year = options.year
cours = options.cours
save_file_name = './csv_out/' + "anime_" + year + "_C" + cours + ".csv"

get_date = datetime.now()
param = sys.argv

url = 'https://anime-api.deno.dev/anime/v1/master/' + year + '/' + cours
result = requests.get(url)

master_list = json.loads(result.text)

meta_data_list = []
meta_data_list_db = []
master_ids = []

log_time = datetime.now()


def parse_meta_data(bsObj):

    v = bsObj.find("meta", attrs={"name": "description"})
    description = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"name": "keywords"})
    keywords = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"name": "author"})
    author = v.get("content") if v else ""

    # --------- OGP ------------

    v = bsObj.find("meta", attrs={"property": "og:title"})
    og_title = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property": "og:type"})
    og_type = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property": "og:url"})
    og_url = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property": "og:image"})
    og_image = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property": "og:site_name"})
    og_site_name = v.get("content") if v else ""

    v = bsObj.find("meta", attrs={"property": "og:description"})
    og_description = v.get("content") if v else ""

    id = master['id']
    title = master['title']
    public_url = master['public_url']

    meta_data = {}

    meta_data['bases_id'] = str(id)
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
    meta_data['get_date'] = log_time
    meta_data['created_at'] = log_time
    meta_data['updated_at'] = log_time

    meta_data_list_db.append([str(id), public_url, description, keywords, author,
                              og_title, og_type, og_description, og_url, og_image, og_site_name,
                              log_time, log_time, log_time])

    if save_image_flag and og_image:
        root, ext = os.path.splitext(og_image)
        # extにリクエストパラメータがついている場合があるので?以降を消去
        ext = re.sub(r'\?.*', "", ext)
        save_image_filename = SAVE_OGIMAGE_PATH + meta_data['bases_id'] + ext
        print(og_image + " -> " + save_image_filename)
        try:
            urlretrieve(og_image, save_image_filename)
        except:
            print("ERROR SAVE IMAGE:", sys.exc_info()[0])

    meta_data_list.append(meta_data)


for master in master_list:

    print(master['title'] + " " + master['public_url'])

    master_ids.append(str(master['id']))
    html = None

    try:
        html = requests.get(master['public_url'])
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
        continue

    try:
        bsObj = BeautifulSoup(html.text.encode(html.encoding), "html.parser")
        parse_meta_data(bsObj)
    except:
        # エンコードが認識できないサイトがあるので一度だけリトライする
        print("ERROR!! " + master['public_url'])
        bsObj = BeautifulSoup(html.text.encode('utf8'), "html.parser")
        parse_meta_data(bsObj)


def build_insert_sql(table_name):
    return 'INSERT INTO ' + table_name + ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


ANIME_API_DB_HOST = os.getenv('ANIME_API_DB_HOST', "localhost")
ANIME_API_DB_USER = os.getenv('ANIME_API_DB_USER', "root")
ANIME_API_DB_PASS = os.getenv('ANIME_API_DB_PASS', "")
ANIME_API_DB_DATABASE = os.getenv(
    'ANIME_API_DB_DATABASE', "anime_admin_development")

if register_flag:
    connection = pymysql.connect(host=ANIME_API_DB_HOST,
                                 user=ANIME_API_DB_USER,
                                 password=ANIME_API_DB_PASS,
                                 db=ANIME_API_DB_DATABASE,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    # Statusテーブルを初期化
    with connection.cursor() as cursor:
        sql = "delete FROM site_meta_data WHERE bases_id IN (" + ",".join(
            master_ids) + ")"
        print(sql)
        cursor.execute(sql)
        cursor.executemany(build_insert_sql(
            "site_meta_data"), meta_data_list_db)
        cursor.executemany(build_insert_sql(
            "site_meta_data_histories"), meta_data_list_db)
        connection.commit()

else:
    with open(save_file_name, 'wt') as fout:
        cout = csv.DictWriter(fout, ['bases_id', 'public_url', 'description', 'keywords',
                                     'author', 'og_title', 'og_type', 'og_description', 'og_url', 'og_image',
                                     'og_site_name', 'get_date', 'created_at', 'updated_at'])
        cout.writeheader()
        cout.writerows(meta_data_list)
