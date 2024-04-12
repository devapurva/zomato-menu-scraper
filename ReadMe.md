# Zomato Menu Scraper

This Python script extracts menu data from a Zomato restaurant page and saves it in both JSON and CSV formats.

## Requirements

- Python 3.x
- BeautifulSoup4
- Requests

## How to Run

1. Clone or download the repository.
2. Navigate to the directory containing the script.
3. Install the required dependencies using `pip install -r requirements.txt`.
4. Run the script using `python zomato_menu_scraper.py`.
5. Enter the Zomato link when prompted (e.g., `https://www.zomato.com/mumbai/rasoi-dadar-east`).
6. The script will scrape the webpage, extract menu data, and save it in JSON and CSV formats.

## Script Details

### Libraries Used:
- `json`: For JSON serialization and deserialization.
- `requests`: For making HTTP requests to fetch webpage data.
- `pandas`: For handling data in tabular format.
- `csv`: For reading and writing CSV files.
- `BeautifulSoup`: For parsing HTML content.
- `re`: For regular expression-based pattern matching.
- `html`: For unescaping HTML entities.

### Functions:
- `save_json(name, data)`: Saves JSON data to a file.
- `extract_needed_data(json_data)`: Extracts relevant menu data from JSON.
- `json_to_csv(json_data, csv_filepath)`: Converts JSON data to CSV format.
- `get_menu(url, save=True)`: Scrapes Zomato webpage, extracts data, and saves it.

### Running the Script:
1. The user provides the Zomato link.
2. The script fetches the webpage.
3. HTML content is parsed to find menu data.
4. Menu data is extracted and saved in JSON and CSV formats.
5. Output files are named after the restaurant.

## Additional Comments:
- The script uses a user-agent header to mimic a web browser's request.
- It extracts menu data using regular expressions to find JSON content embedded in the webpage.
- The extracted data includes menu names, categories, item names, prices, descriptions, and dietary slugs.

