from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import pickle

current_url = 'https://www.hemnet.se/salda/bostader'

all_url = ['https://www.hemnet.se/salda/bostader']

for i in range(49):
    next_url = current_url+"?page="+str(i+2)
    all_url.append(next_url)


###########

# Saving each house type in a seperate list
Fritidshus = []
Lägenhet = []
Villa = []
Parhus = []
Tomt = []
Radhus = []
Gård_skog = []
Övrig = []
Kedjehus = []
Par_kedje_radhus = []


def main():
    s = Service(
        "/Users/siddheshsreedar/Downloads/chromedriver-mac-arm64/chromedriver")
    for url in all_url:
        print(url)
        for i in range(3):  # Retry 3 times if an error occurs
            try:
                abc = [
                    url
                ]
                for final in abc:
                    driver = webdriver.Chrome(service=s)
                    driver.get(final)
                houses_link = []

                product_elements = driver.find_elements(
                    By.CLASS_NAME, 'hcl-card')
                for element in product_elements:
                    href = element.get_attribute('href')
                    if href:
                        houses_link.append(href)
                driver.quit()
                houses_link = houses_link[2:]
                for i in houses_link:
                    data = extract_data(i)
                    category = data[1].split("-")[0][:-1]
                    if category == "Fritidshus":
                        Fritidshus.append(data)
                    elif category == "Lägenhet":
                        Lägenhet.append(data)
                    elif category == "Villa":
                        Villa.append(data)
                    elif category == "Parhus":
                        Parhus.append(data)
                    elif category == "Tomt":
                        Tomt.append(data)
                    elif category == "Gård_skog":
                        Gård_skog.append(data)
                    elif category == "Övrig":
                        Övrig.append(data)
                    elif category == "Kedjehus":
                        Kedjehus.append(data)
                    elif category == "Par_kedje_radhus":
                        Par_kedje_radhus.append(data)
                break
            except Exception as e:
                print("Error:", e)
                print("Retrying...")


def extract_data(url):
    s = Service(
        "/Users/siddheshsreedar/Downloads/chromedriver-mac-arm64/chromedriver")
    data = []
    driver = webdriver.Chrome(service=s)
    driver.get(url)
    try:
        name = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "hcl-heading")))
        data.append(name.text)

        location_sold = driver.find_elements(By.TAG_NAME, 'p')
        data.append(location_sold[0].text)

        elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//strong[@translate='yes' and contains(@class, 'hcl-text--medium')]")))
        for element in elements:
            text = element.get_attribute('innerText').replace('\xa0', ' ')
            data.append(text)
    except:
        print("An error occurred. Refreshing the page...")
        driver.refresh()
        # Wait for the page to load after refreshing
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "hcl-heading")))
        # Retry extracting data
        return extract_data(url)
    finally:
        driver.quit()
    return data


if __name__ == "__main__":
    main()
    lägenhet_df = pd.DataFrame(Lägenhet)
    lägenhet_df.to_csv('lägenhet_data.csv', index=False)

    Villa_df = pd.DataFrame(Villa)
    Villa_df.to_csv('Villa_df.csv', index=False)

    Fritidshus_df = pd.DataFrame(Fritidshus)
    Fritidshus_df.to_csv('Fritidshus_df.csv', index=False)

    Parhus_df = pd.DataFrame(Parhus)
    Parhus_df.to_csv('Parhus_df.csv', index=False)

    Tomt_df = pd.DataFrame(Tomt)
    Tomt_df.to_csv('Tomt_df.csv', index=False)

    Radhus_df = pd.DataFrame(Radhus)
    Radhus_df.to_csv('Radhus_df.csv', index=False)

    Gård_skog_df = pd.DataFrame(Gård_skog)
    Gård_skog_df.to_csv('Gård_skog_df.csv', index=False)

    Övrig_df = pd.DataFrame(Övrig)
    Övrig_df.to_csv('Övrig_df.csv', index=False)

    Kedjehus_df = pd.DataFrame(Kedjehus)
    Kedjehus_df.to_csv('Kedjehus_df.csv', index=False)

    Par_kedje_radhus_df = pd.DataFrame(Par_kedje_radhus)
    Par_kedje_radhus_df.to_csv('Par_kedje_radhus_df.csv', index=False)
