# Epidemics Data Scraper

A Scrapy project that extracts historical epidemic data from Wikipedia, including disease details, mortality statistics, and outbreak information.

## 📌 Project Overview

This project consists of:
- Web spider that crawls Wikipedia's List of Epidemics page
- Data cleaning pipeline for quality control
- Structured data output in JSON format
- Deduplication and validation mechanisms

## ✨ Features

- Extracts epidemic data from both list pages and individual disease pages
- Collects:
  - Disease names
  - Outbreak dates
  - Death tolls
  - Confirmed cases
  - Historical context
  - Wikipedia article URLs
- Automated data filtering:
  - Removes entries before 1960
  - Prevents duplicate entries
  - Handles missing data gracefully

## 🛠 Requirements

- Python 3.7+
- Scrapy 2.5+
- pip package manager

## 🚀 Installation

1. Clone repository:
```bash
git clone https://github.com/<your-username>/epidemics-scraper.git
cd epidemics-scraper
```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

📊 Usage :
 Run the spider:
 ```bash
scrapy crawl infos -O output.json
```
Output will be saved in:

* output.json (JSON format)

🗂 Project Structure:
```bash
epidemics-scraper/
├── scrapy.cfg
├── diseases/
│   ├── __init__.py
│   ├── items.py         # Data structure definition
│   ├── pipelines.py     # Data cleaning and validation
│   ├── settings.py      # Scrapy configuration
│   └── spiders/
│       └── infos.py     # Main spider implementation
```

⚙ Configuration 

Key settings in settings.py:
 ```bash
ITEM_PIPELINES = {
    'diseases.pipelines.DiseasesPipeline': 300,
}
FEED_FORMAT = 'json'
FEED_EXPORT_ENCODING = 'utf-8'
```




