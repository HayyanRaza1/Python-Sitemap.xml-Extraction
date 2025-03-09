# XML Sitemap Crawler & Google Sheets Updater

## 📌 Overview
This Python script crawls a website's XML sitemap, categorizes URLs into different types, and updates a Google Sheet with the structured data. 

## 🚀 Features
- Fetches URLs from XML sitemaps (including nested sitemap indexes)
- Categorizes URLs into predefined types (Home Page, Money Pages, Product Pages, etc.)
- Ignores unwanted URLs like login, cart, checkout, and WordPress-related paths
- Updates a Google Sheet while preserving headers
- Handles API rate limits with automatic retries

## 📂 Requirements
- Python 3.x
- A Google Service Account JSON keyfile (for Sheets API authentication)
- The following Python libraries:
  ```bash
  pip install requests gspread beautifulsoup4 oauth2client lxml
  ```

## 🛠️ Setup
### 1️⃣ Get Your Google Sheets API Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the Google Sheets API.
3. Create a Service Account and generate a JSON keyfile.
4. Share your Google Sheet with the service account email.

### 2️⃣ Run the Script
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/repository-name.git
   ```
2. Navigate to the project folder:
   ```bash
   cd repository-name
   ```
3. Place your `credentials.json` file in the project directory.
4. Run the script:
   ```bash
   python script.py
   ```

## 🏗️ How It Works
1. **User Input:** The script prompts for the Google Sheet ID, sheet tab name, and website URL.
2. **Fetching Sitemap:** It retrieves all URLs from the XML sitemap (including sub-sitemaps).
3. **Categorization:** URLs are classified into different types based on predefined rules.
4. **Google Sheets Update:** The categorized URLs are uploaded to the specified Google Sheet.
5. **Retry Logic:** Handles Google Sheets API limits by retrying failed requests.

## 🎯 URL Categories
- **Home Page**: The main website page
- **Money Pages**: Key service or collection pages
- **Location Pages**: Pages containing `/location`
- **Product Pages**: Pages containing `/product`
- **Industry Pages**: Pages containing `/industry`
- **Blog & News Pages**: Pages containing `/blog` or `/news`
- **Other Pages**: Uncategorized URLs

## 📝 Notes
- Ensure your Google Sheet has headers before running the script.
- Make sure your service account has `Editor` access to the Google Sheet.

## 🏆 Contributing
Feel free to fork this repo, submit issues, or contribute with pull requests!

## 📜 License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
🔗 **Author:** Syed Hayyan Raza  
