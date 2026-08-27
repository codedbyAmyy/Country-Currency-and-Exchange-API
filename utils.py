import requests
import os
import random
from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("REST_COUNTRIES_API_KEY")
REFRESH_TIMEOUT = int(os.getenv("REFRESH_TIMEOUT", "30"))
CACHE_IMAGE_PATH = os.getenv("CACHE_IMAGE_PATH", "cache/summary.png")

RESTCOUNTRIES_URL = "https://api.restcountries.com/countries/v5?response_fields=names,capitals,region,population,currencies,flag&pretty=1"
EXCHANGE_RATES_URL = "https://open.er-api.com/v6/latest/USD"

def fetch_countries():
    base_url = "https://api.restcountries.com/countries/v5"
    fields = "names,capitals,region,population,currencies,flag"
    limit = 100
    offset = 0
    all_countries = []
    
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        while True:
            paginated_url = f"{base_url}?response_fields={fields}&limit={limit}&offset={offset}"
            
            resp = requests.get(paginated_url, headers=headers, timeout=REFRESH_TIMEOUT)
            resp.raise_for_status()
            data = resp.json()
            
            if isinstance(data, dict):
                page_results = data.get("data", {}).get("objects", [])
            else:
                page_results = data
                
            if not page_results:
                break 
            all_countries.extend(page_results)
            
            # If the page returns fewer than 100 items, we reached the end
            if len(page_results) < limit:
                break
            offset += limit
        return all_countries
    except Exception as e:
        raise RuntimeError(f"Countries API error: {e}")
    
def fetch_exchange_rates():
    try:
        resp = requests.get(EXCHANGE_RATES_URL, timeout=REFRESH_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        if data.get("result") == "success":
            return data.get("rates", {})
        return data.get("rates", {})
    except Exception as e:
        raise RuntimeError(f"Exchange API error: {e}")

def compute_estimated_gdp(population, exchange_rate):
    if population is None or exchange_rate in (None, 0):
        return None
    multiplier = random.randint(1000, 2000)
    return (population * multiplier) / exchange_rate

def generate_summary_image(total, top5, timestamp, out_path=CACHE_IMAGE_PATH):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    width, height = 1200, 675
    im = Image.new("RGB", (width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)

    try:
        font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        font_text = ImageFont.truetype("DejaVuSans.ttf", 20)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    margin = 40
    y = margin
    draw.text((margin, y), f"Countries Refresh Summary", font=font_title, fill=(0, 0, 0))
    y += 50
    draw.text((margin, y), f"Total countries: {total}", font=font_text, fill=(0, 0, 0))
    y += 30
    draw.text((margin, y), f"Top 5 by estimated GDP:", font=font_text, fill=(0, 0, 0))
    y += 30

    for i, c in enumerate(top5, start=1):
        name = c.get("name")
        gdp = c.get("estimated_gdp") or 0
        draw.text((margin + 20, y), f"{i}. {name} — {gdp:,.2f}", font=font_text, fill=(0, 0, 0))
        y += 26

    y += 10
    draw.text((margin, y), f"Last refreshed at (UTC): {timestamp}", font=font_text, fill=(0, 0, 0))

    im.save(out_path)
    return out_path
