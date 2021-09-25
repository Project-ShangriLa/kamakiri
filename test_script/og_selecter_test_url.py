from bs4 import BeautifulSoup
import sys
import requests

argv = sys.argv
url = argv[1]

html = requests.get(url)
bs_obj = BeautifulSoup(html.text.encode(html.encoding), "html.parser")

v = bs_obj.find("meta", attrs={"property":"og:title"})
og_title = v.get("content") if v else ""

v = bs_obj.find("meta", attrs={"property":"og:type"})
og_type = v.get("content") if v else ""

v = bs_obj.find("meta", attrs={"property":"og:url"})
og_url = v.get("content") if v else ""

v = bs_obj.find("meta", attrs={"property":"og:image"})
og_image = v.get("content") if v else ""

v = bs_obj.find("meta", attrs={"property":"og:site_name"})
og_site_name = v.get("content") if v else ""

v = bs_obj.find("meta", attrs={"property":"og:description"})
og_description = v.get("content") if v else ""

print('      og_title:', og_title)
print('       og_type:', og_type)
print('        og_url:', og_url)
print('      og_image:', og_image)
print('  og_site_name:', og_site_name)
print('og_description:', og_description)
