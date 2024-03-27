from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def scrape_grailed():
    # Set up Selenium WebDriver
    options = Options()
    # options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.grailed.com/shop/yswa-3w-gw")

    sleep(4)
    # Initialize data storage
    data = {"Name": [], "Price": [], "Image URL": [], "Link": []}

    # Wait for the items to load and find all item containers
    items = driver.find_elements(By.CSS_SELECTOR, ".feed-item")

    for item in items:
        # Get item details
        try:
            name_element = item.find_element(
                By.CSS_SELECTOR, ".ListingMetadata-module__title___Rsj55"
            )
            price_element = item.find_element(
                By.CSS_SELECTOR,
                ".Price-module__onSale___1pIHp, .Price-module__root___dK0sQ",
            )
            image_element = item.find_element(
                By.CSS_SELECTOR, ".listing-cover-photo img"
            )
            link_element = item.find_element(By.CSS_SELECTOR, "a.listing-item-link")

            name = name_element.text if name_element else "No Name"
            price = price_element.text if price_element else "No Price"
            image_url = (
                image_element.get_attribute("src") if image_element else "No Image URL"
            )
            link = link_element.get_attribute("href") if link_element else "No Link"

            data["Name"].append(name)
            data["Price"].append(price)
            data["Image URL"].append(image_url)
            data["Link"].append(link)
        except Exception as e:
            print(f"Error extracting item details: {e}")

    driver.quit()

    # Convert data to DataFrame
    return pd.DataFrame(data)


if __name__ == "__main__":
    items_data = scrape_grailed()
    print(items_data)
    items_data.to_csv("grailed_items.csv", index=False)
