import requests
from bs4 import BeautifulSoup
import urllib.parse
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cairosvg  # Required for SVG conversion

# Headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# List of URLs to scrape
urls = [
    'https://autosecuritas-ct-seysses.fr/public/',
    'https://www.ebayglobalshipping.com/',
    'https://renault-tortosa.es/',
    'https://ford.pl.ua/',
    'https://www.kia-suedmobile-radolfzell.de/',
    'https://subaru.nc/',
    'https://renaulttersa.com.mx/',
    'https://wurthsaudi.com/'
]

def find_logo(soup, base_url):
    """
    Extracts the most probable logo from the website.
    """
    # List of common logo locations
    possible_tags = [
        ("a", "navbar-brand"),  
        ("div", "site-branding"),
        ("header", None),  
        ("img", "logo"),  
        ("div", "header-logo"),
        ("div", "header"),
        ("div", "element-widget-container"),
        ("div","logo")
    ]
    
    for tag, class_name in possible_tags:
        if class_name:
            element = soup.find(tag, class_=class_name)
        else:
            element = soup.find(tag)

        if element:
            logo_img = element.find("img")
            if logo_img and logo_img.get("src"):
                return urllib.parse.urljoin(base_url, logo_img["src"])

    # Fallback: Any <img> with 'logo' in alt or class
    for img_tag in soup.find_all("img"):
        if "logo" in (img_tag.get("alt") or "").lower() or "logo" in (img_tag.get("class") or []):
            return urllib.parse.urljoin(base_url, img_tag["src"])

    return None  # No logo found


def fetch_and_process_logo(url):
    """
    Fetches the logo from a given URL, downloads it, and processes it.
    """
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch website {url}. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    logo_url = find_logo(soup, url)
    
    if not logo_url:
        print(f"No logo found for {url}")
        return None

    parsed_url = urllib.parse.urlparse(logo_url)
    logo_name = os.path.basename(parsed_url.path)

    # Download the logo
    img_response = requests.get(logo_url, headers=headers)
    if img_response.status_code != 200:
        print(f"Failed to download logo from {url}. Status code: {img_response.status_code}")
        return None

    # Save the logo to a file
    with open(logo_name, "wb") as f:
        f.write(img_response.content)

    # Convert SVG to PNG if necessary
    if logo_name.endswith('.svg'):
        png_logo_name = logo_name.replace('.svg', '.png')
        cairosvg.svg2png(url=logo_name, write_to=png_logo_name)
        logo_name = png_logo_name

    return logo_name


# Fetch and process logos for all URLs
logo_files = []
for url in urls:
    logo_file = fetch_and_process_logo(url)
    if logo_file:
        logo_files.append(logo_file)

# Display logos using matplotlib with a dynamic grid
if logo_files:
    num_logos = len(logo_files)
    cols = 3  # Number of columns per row (adjustable)
    rows = (num_logos // cols) + (num_logos % cols > 0)  # Calculate rows dynamically

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 3, rows * 3))  # Adjust figure size

    # Flatten axes array for easy indexing
    axes = axes.flatten() if num_logos > 1 else [axes]

    for i, logo_file in enumerate(logo_files):
        img = mpimg.imread(logo_file)
        axes[i].imshow(img)
        axes[i].axis("off")
        axes[i].set_title(f"Logo {i+1}")

    # Hide any unused subplot spaces
    for j in range(i + 1, len(axes)):
        axes[j].axis("off")

    plt.tight_layout()
    plt.show()
else:
    print("No logos were fetched.")