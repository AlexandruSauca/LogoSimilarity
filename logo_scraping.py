import ssl
import urllib.request
import urllib.parse
import urllib.error  # Import error handling
from bs4 import BeautifulSoup

# Disable SSL verification (if needed)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Define the website URL
url = 'https://www.astrazeneca.ua/'

# Set a User-Agent to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    # Create a request with headers
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req, context=ctx)
    html = response.read()
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code} - {e.reason}")
    exit()
except urllib.error.URLError as e:
    print(f"Failed to open URL: {e.reason}")
    exit()

# Parse the webpage
soup = BeautifulSoup(html, 'html.parser')

# Find all <img> tags
images = soup.find_all('img')

# Try to find the logo based on keywords in the image URL
logo_url = None
for img in images:
    img_src = img.get('src')
    if img_src and ('logo' in img_src.lower() or 'astrazeneca' in img_src.lower()):
        logo_url = img_src
        break  # Stop at the first match

# Check if we found a logo
if logo_url:
    # Convert relative URL to absolute if necessary
    if not logo_url.startswith("http"):
        logo_url = urllib.parse.urljoin(url, logo_url)
    
    print(f"Logo found: {logo_url}")

    try:
        # Try to download and save the logo
        urllib.request.urlretrieve(logo_url, "astrazeneca_logo.jpg")
        print("Logo saved as astrazeneca_logo.jpg")
    except urllib.error.URLError as e:
        print(f"Failed to download the logo: {e.reason}")

else:
    print("No logo found on the page.")
