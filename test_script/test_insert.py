import pymysql.cursors
import os


def build_insert_sql(table_name):
    return 'INSERT INTO ' + table_name + ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'


ANIME_API_DB_HOST = os.getenv('ANIME_API_DB_HOST', "localhost")
ANIME_API_DB_USER = os.getenv('ANIME_API_DB_USER', "root")
ANIME_API_DB_PASS = os.getenv('ANIME_API_DB_PASS', "")
ANIME_API_DB_DATABASE = os.getenv(
    'ANIME_API_DB_DATABASE', "anime_admin_development")

connection = pymysql.connect(host=ANIME_API_DB_HOST,
                             user=ANIME_API_DB_USER,
                             password=ANIME_API_DB_PASS,
                             db=ANIME_API_DB_DATABASE,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
    cursor.execute(build_insert_sql("site_meta_data"), (1442, 	"https://kimetsu.com/anime/", "「がんばれ同期ちゃん」とは、空回りしつつも既成事実を作る為にひたすらがんばる同期ちゃんのお話である。", "",
    	"アニメ「鬼滅の刃」公式ポータルサイト","アニメ「鬼滅の刃」公式ポータルサイト",	"website",	"アニメ「鬼滅の刃」公式ポータルサイト",
            	"https://kimetsu.com/anime/",	"https://kimetsu.com/anime/ogp.png","",
                		"2021-09-26 12:20:23.041337",	"2021-09-26 12:20:23.041337",
                        	"2021-09-26 12:20:23.041337"))

    cursor.executemany(build_insert_sql("site_meta_data"), [(1443, 	"https://kimetsu.com/anime/", "「がんばれ同期ちゃん」とは、空回りしつつも既成事実を作る為にひたすらがんばる同期ちゃんのお話である。", "",
    	"アニメ「鬼滅の刃」公式ポータルサイト","アニメ「鬼滅の刃」公式ポータルサイト",	"website",	"アニメ「鬼滅の刃」公式ポータルサイト",
            	"https://kimetsu.com/anime/",	"https://kimetsu.com/anime/ogp.png","",
                		"2021-09-26 12:20:23.041337",	"2021-09-26 12:20:23.041337",
                        	"2021-09-26 12:20:23.041337"),
                            (1444, 	"https://kimetsu.com/anime/", "「がんばれ同期ちゃん」とは、空回りしつつも既成事実を作る為にひたすらがんばる同期ちゃんのお話である。", "",
    	"アニメ「鬼滅の刃」公式ポータルサイト","アニメ「鬼滅の刃」公式ポータルサイト",	"website",	"アニメ「鬼滅の刃」公式ポータルサイト",
            	"https://kimetsu.com/anime/",	"https://kimetsu.com/anime/ogp.png","",
                		"2021-09-26 12:20:23.041337",	"2021-09-26 12:20:23.041337",
                        	"2021-09-26 12:20:23.041337")
                            ])
    connection.commit()
