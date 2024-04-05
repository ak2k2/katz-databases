from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def main():
    options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    columns = ["Name", "Description", "Price", "Image URLs"]
    data = pd.DataFrame(columns=columns)

    try:
        driver.get("https://us.supreme.com/pages/shop")
        sleep(1)

        product_elements = driver.find_elements(
            By.CSS_SELECTOR, "li.bg-gray--2 a[data-navigate]"
        )
        product_urls = [element.get_attribute("href") for element in product_elements]

        print(f"Found {len(product_urls)} products")

        for url in product_urls[:1]:
            driver.get(url)
            sleep(1)

            # Item Name
            name = wait.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "h1.product-title"))
            ).text

            # Item Description
            description = driver.find_element(
                By.CSS_SELECTOR, 'div[itemprop="description"]'
            ).text

            # Item Price
            price = driver.find_element(By.CSS_SELECTOR, 'div[itemprop="price"]').text

            # Item Image URL(s)
            image_elements = driver.find_elements(
                By.CSS_SELECTOR, "img.js-product-image"
            )
            image_urls = [img.get_attribute("src") for img in image_elements]

            new_row = pd.DataFrame(
                [
                    {
                        "Name": name,
                        "Description": description,
                        "Price": price,
                        "Image URLs": image_urls,
                    }
                ]
            )
            data = pd.concat([data, new_row], ignore_index=True)

    finally:
        driver.quit()

    return data


if __name__ == "__main__":
    data = main()
    data.to_csv(
        "scraped_item_listings/supreme_products_wa_20230404055653.csv", index=False
    )
