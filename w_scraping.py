import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, SVG
import webbrowser
from cairosvg import svg2png


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = 'https://autosecuritas-ct-seysses.fr/public/'

response = requests.get(url, headers=headers)
if response.status_code != 200:
    print(f"Failed to fetch website. Status code:{response.status_code}")
    exit()
print(response.status_code)

soup =  BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find('img')
if img_tags is None:
    print("No image found")
    exit()
print(img_tags)

logo_url = img_tags['src']
print(logo_url)

full_logo = urllib.parse.urljoin(url , logo_url)
print(full_logo)

parsed_url = urllib.parse.urlparse(full_logo)
logo_name = os.path.basename(parsed_url.path)
print(logo_name)

img_response = requests.get(full_logo , headers=headers)
print(img_response.status_code)

if img_response.status_code != 200:
    print(f"Failed to download logo. Status code: {img_response.status_code}")
    exit()

with open(logo_name, "wb") as f:
    f.write(img_response.content)

display(SVG(full_logo))


png_logo_name = logo_name.replace('.svg', '.png')
svg2png(url=logo_name, write_to=png_logo_name)

print(png_logo_name)

img = mpimg.imread(png_logo_name) 
plt.imshow(img) 
plt.axis("off") 
plt.show()