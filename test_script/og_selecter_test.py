
from bs4 import BeautifulSoup
import sys
from pprint import pprint

argvs = sys.argv

input_file = argvs[1]

html = open(input_file)

bsObj = BeautifulSoup(html.read(), "html.parser")

v = bsObj.find("meta", attrs={"property":"og:title"})
og_title = v.get("content")

v = bsObj.find("meta", attrs={"property":"og:type"})
og_type = v.get("content")

v = bsObj.find("meta", attrs={"property":"og:url"})
og_url = v.get("content")

v = bsObj.find("meta", attrs={"property":"og:image"})
og_image = v.get("content")

v = bsObj.find("meta", attrs={"property":"og:site_name"})
og_site_name = v.get("content")

v = bsObj.find("meta", attrs={"property":"og:description"})
og_description = v.get("content")


print('og_title,og_type,og_url,og_image,og_site_name,og_description')

print(','.join([og_title, og_type, og_url, og_image, og_site_name, og_description]))
