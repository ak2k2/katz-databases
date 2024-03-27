from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd


def scrape_grailed():
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.grailed.com/shop/yswa-3w-gw")

    start_time = time.time()
    # Simulate scrolling to load all items
    while time.time() - start_time < 50:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    data = {"Name": [], "Price": [], "Image URL": [], "Link": []}

    items = driver.find_elements(By.CSS_SELECTOR, ".feed-item:not(.empty-item)")
    for item in items:
        try:
            time.sleep(0.1)
            link_element = item.find_elements(By.CSS_SELECTOR, "a.listing-item-link")
            title_element = item.find_elements(
                By.CSS_SELECTOR, ".ListingMetadata-module__title___Rsj55"
            )
            price_element = item.find_elements(
                By.CSS_SELECTOR, ".Price-module__onSale___1pIHp"
            )
            image_element = item.find_elements(
                By.CSS_SELECTOR, ".listing-cover-photo img"
            )

            if link_element and title_element and price_element and image_element:
                data["Name"].append(title_element[0].text)
                data["Price"].append(price_element[0].text)
                data["Image URL"].append(image_element[0].get_attribute("src"))
                data["Link"].append(link_element[0].get_attribute("href"))
        except Exception as e:
            print(f"Error extracting item details: {e}")

    driver.quit()
    return pd.DataFrame(data)


df = scrape_grailed()
df.to_csv("grailed_long.csv", index=False)
