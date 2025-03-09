import requests
import gspread
import time
from bs4 import BeautifulSoup
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import APIError

# Function to get user inputs
def get_user_inputs():
    sheet_id = input("Enter your Google Sheet ID: ").strip()
    tab_name = input("Enter the Sheet Tab Name: ").strip()
    return sheet_id, tab_name

# Function to authenticate Google Sheets API
def authenticate_google_sheets(json_keyfile):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    return gspread.authorize(creds)

# Function to fetch and parse XML sitemap
def fetch_xml_sitemap(sitemap_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    print(f"🔍 Checking XML sitemap: {sitemap_url}")

    try:
        response = requests.get(sitemap_url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return []

    if response.status_code != 200:
        print(f"❌ Failed to fetch XML sitemap ({response.status_code})")
        return []

    soup = BeautifulSoup(response.text, "lxml-xml")

    if soup.find("sitemapindex"):
        urls = []
        print("📂 Sitemap index detected. Fetching sub-sitemaps...")
        for loc in soup.find_all("loc"):
            urls.extend(fetch_xml_sitemap(loc.text.strip()))
        return urls

    return [loc.text.strip() for loc in soup.find_all("loc")]

# Function to categorize and filter URLs
def categorize_urls(urls, base_url):
    categories = {
        "Home Page": lambda url: url == base_url,
        "Money Pages": lambda url: any(x in url for x in ["/services", "/collection"]),
        "Location Pages": lambda url: "/location" in url,
        "Product Pages": lambda url: "/product" in url,
        "Industry Pages": lambda url: "/industry" in url,
        "Blog & News Pages": lambda url: any(x in url for x in ["/blog", "/news"]),
    }

    filtered_urls = {category: [] for category in categories}
    filtered_urls["Other Pages"] = []

    ignore_keywords = [
        "login", "account", "cart", "checkout", "privacy", "terms", "faq", "contact",
        "wp-content", "wp-includes", "wp-json"  # WordPress-related URLs to ignore
    ]

    for url in urls:
        if any(kw in url.lower() for kw in ignore_keywords):  # Convert to lowercase for case insensitivity
            continue

        added = False
        for category, condition in categories.items():
            if condition(url):
                filtered_urls[category].append(url)
                added = True
                break

        if not added:
            filtered_urls["Other Pages"].append(url)

    return filtered_urls

# Function to update Google Sheet without modifying headers
def update_google_sheet(sheet_id, tab_name, data, json_keyfile, base_url):
    client = authenticate_google_sheets(json_keyfile)
    sheet = client.open_by_key(sheet_id).worksheet(tab_name)
    
    # Ensure the Home Page is in the second row
    rows = [["Home Page", base_url]]
    for category in ["Money Pages", "Location Pages", "Product Pages", "Industry Pages", "Blog & News Pages", "Other Pages"]:
        for url in data[category]:
            rows.append([category, url])
    
    retry_attempts = 3
    for attempt in range(retry_attempts):
        try:
            sheet.update("A2", rows)  # Start from A2 to keep headers intact
            print(f"✅ Data updated successfully in '{tab_name}'!")
            return
        except APIError as e:
            if "Quota exceeded" in str(e) and attempt < retry_attempts - 1:
                print("⏳ Quota exceeded. Retrying in 60 seconds...")
                time.sleep(60)
            else:
                print(f"❌ API Error: {e}")
                return

# Main Execution
if __name__ == "__main__":
    JSON_KEYFILE = "credentials.json"

    sheet_id, tab_name = get_user_inputs()
    base_url = input("Enter the website URL (e.g., https://example.com): ").strip().rstrip("/")

    xml_sitemap_urls = fetch_xml_sitemap(f"{base_url}/sitemap_index.xml") or fetch_xml_sitemap(f"{base_url}/sitemap.xml")

    all_urls = list(set(xml_sitemap_urls))

    if not all_urls:
        print("❌ No important pages found. Exiting.")
        exit()

    print("📌 Categorizing and filtering URLs...")
    categorized_urls = categorize_urls(all_urls, base_url)

    print(f"📊 Updating Google Sheet tab: {tab_name}...")
    update_google_sheet(sheet_id, tab_name, categorized_urls, JSON_KEYFILE, base_url)
