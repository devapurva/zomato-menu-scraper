import os
import json
import requests
import pandas as pd
import csv
from bs4 import BeautifulSoup
import re
from html import unescape

# User-agent header to mimic a web browser's request
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'}

def save_json(name, data):
    """ Save the JSON data """
    with open(f"{name}.json", "w") as file:
        json.dump(data, file, indent=4)

def extract_needed_data(json_data):
    """ Extracts only the relevant data for CSV conversion """
    if isinstance(json_data, str):
        # If the data is still a string, it might be double-encoded JSON
        json_data = json.loads(json_data)
    # Extract the resId
    resId = str(json_data.get("pages", {}).get('current', {}).get("resId"))
    # Use the resId to access the menus
    menus = json_data.get("pages", {}).get('restaurant', {}).get(resId, {}).get("order", {}).get("menuList", {}).get("menus", [])
    name = json_data.get("pages", {}).get('restaurant', {}).get(resId, {}).get("sections", {}).get("SECTION_BASIC_INFO", {}).get('name')
    
    # Filter out only the relevant data for CSV conversion
    filtered_menus = []
    for menu in menus:
        filtered_menu = {
            "name": menu.get("menu", {}).get("name", ""),  # Correctly extract menu name
            "category": []
        }
        for category in menu.get("menu", {}).get("categories", []):
            filtered_category = {
                "name": category.get("category", {}).get("name", ""),  # Correctly extract category name
                "items": []
            }
            for item in category.get("category", {}).get("items", []):
                filtered_item = {
                    "name": item["item"]["name"],
                    "price": item["item"]["display_price"],
                    "desc": item["item"]["desc"],
                    "dietary_slugs": ','.join(item["item"].get("dietary_slugs", []))  # Combine dietary_slugs into a single string
                }
                filtered_category["items"].append(filtered_item)
            filtered_menu["category"].append(filtered_category)
        filtered_menus.append(filtered_menu)
    
    return {'name': name, 'menus': filtered_menus}

def json_to_csv(json_data, csv_filepath):
    """ Convert JSON data to CSV """
    # Prepare CSV data
    csv_data = []
    for menu in json_data.get("menus", []):
        for category in menu.get("category", []):
            for item in category.get("items", []):
                item_name = item["name"]
                price = item["price"]
                desc = item["desc"]
                dietary_slugs = item["dietary_slugs"]
                # Add row to CSV data including dietary_slugs
                csv_data.append([json_data["name"], menu["name"], category["name"],  dietary_slugs, item_name, price, desc])

    # Write data to CSV
    with open(csv_filepath, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Restaurant", "Menu", "Category", "Veg/NonVeg", "Item Name", "Price", "Description"])
        writer.writerows(csv_data)

def get_menu(url, save=True):
    """ Get all Menu Items from the passed URL """
    global headers
    url += '/order'
    
    # Request for the webpage
    try:
        webpage = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.ReadTimeout:
        print(f"Request timed out for URL: {url}")
        
    html_text = BeautifulSoup(webpage.text, 'html.parser')
    
    scripts = html_text.find_all('script')  # Make sure you define `scripts`
    for script in scripts:
        if 'window.__PRELOADED_STATE__' in script.text:
            # Find the JSON.parse argument
            match = re.search(r'window\.__PRELOADED_STATE__ = JSON\.parse\((.+?)\);', script.text)
            if match:
                # Extract the matched group which is the argument to JSON.parse
                json_str_escaped = match.group(1)
                # Unescape the string to convert it to a proper JSON format
                json_str = unescape(json_str_escaped)
                # The string is double-encoded, so we decode it again
                try:
                    json_str = json.loads(json_str)
                    preloaded_state = json.loads(json_str)
                    # Extract only the needed data from preloaded_state
                    needed_data = extract_needed_data(preloaded_state)
                    name = str(needed_data.get('name'))
                    # Save the JSON data to a file
                    if save:
                        save_json(name, needed_data)
                        save_json('preloaded', preloaded_state)
                    # Convert JSON to CSV
                    json_to_csv(needed_data, f"{name}.csv")
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)
                
    restaurant_name = html_text.head.find('title').text[:-22]

    return restaurant_name

if __name__ == "__main__":
    link = input("Enter the Zomato link (ex:https://www.zomato.com/mumbai/rasoi-dadar-east): ")
    dframe = get_menu(link, save=True)
