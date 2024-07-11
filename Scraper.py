from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
# import pickle
import numpy as np
# import warnings
from datetime import datetime
import locale
import statistics
import json
import mysql.connector
import os


db_sql = os.getenv('DB_SQL')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

current_url = 'https://www.hemnet.se/salda/bostader'

all_url = ['https://www.hemnet.se/salda/bostader']

chrome_driver_path = '/usr/lib/chromium-browser/chromedriver'


for i in range(10):
    next_url = current_url+"?page="+str(i+2)
    all_url.append(next_url)


###########

# Saving each house type in a seperate list
Fritidshus = []
Lägenhet = []
Villa = []
Kedjehus = []
Parhus = []
Tomt = []


def main():
    # s = Service("/Users/siddheshsreedar/Downloads/chromedriver-mac-arm64/chromedriver")
    for url in all_url:
        print(url)
        for i in range(3):  # Retry 3 times if an error occurs
            try:
                abc = [
                    url
                ]
                for final in abc:
                    # driver = webdriver.Chrome(service=s)
                    service = Service(chrome_driver_path)
                    chrome_options = Options()
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument('--no-sandbox')
                    chrome_options.add_argument('--disable-dev-shm-usage')
                    driver = webdriver.Chrome(
                        service=service, options=chrome_options)
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
                    elif category == "Kedjehus":
                        Kedjehus.append(data)

                break
            except Exception as e:
                print("Error:", e)
                print("Retrying...")


def extract_data(url):
    # s = Service("/Users/siddheshsreedar/Downloads/chromedriver-mac-arm64/chromedriver")
    data = []
    service = Service(chrome_driver_path)
    chrome_options = Options()
    # driver = webdriver.Chrome(service=s)
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(
        service=service, options=chrome_options)
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
Kedjehus_df = pd.DataFrame(Kedjehus)
Kedjehus_df.to_csv('Kedjehus_df.csv', index=False)


#################################

#### CLEANING#####################

#################################

def handle_empty_dataframe(df, columns):
    """
    Handle empty DataFrame by creating a DataFrame with a single row of NaN values.
    """
    if df.empty:
        df = pd.DataFrame([np.nan] * len(columns)).T
        df.columns = columns
    else:
        # Ensure columns match expected columns
        df.columns = columns[:len(df.columns)]
    return df


# Example usage for each DataFrame
try:
    df1 = pd.read_csv("lägenhet_data.csv")
except pd.errors.EmptyDataError:
    df1 = handle_empty_dataframe(pd.DataFrame(), [
                                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'])

try:
    df2 = pd.read_csv("Villa_df.csv")
except pd.errors.EmptyDataError:
    df2 = handle_empty_dataframe(pd.DataFrame(), [
                                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'])

try:
    df3 = pd.read_csv("Fritidshus_df.csv")
except pd.errors.EmptyDataError:
    df3 = handle_empty_dataframe(pd.DataFrame(), [
                                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', 'Unnamed: 15'])

try:
    df4 = pd.read_csv("Parhus_df.csv")
except pd.errors.EmptyDataError:
    df4 = handle_empty_dataframe(pd.DataFrame(), [
                                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '8.1', '10', '11', '12', '13', '14', '15'])

try:
    df5 = pd.read_csv("Tomt_df.csv")
except pd.errors.EmptyDataError:
    df5 = handle_empty_dataframe(
        pd.DataFrame(), ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

try:
    df9 = pd.read_csv("Kedjehus_df.csv")
except pd.errors.EmptyDataError:
    df9 = handle_empty_dataframe(pd.DataFrame(), [
                                 '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'])


def ensure_columns(df, expected_columns):
    current_columns = df.columns.tolist()
    if len(current_columns) != len(expected_columns):
        # Calculate the number of missing columns
        num_missing = len(expected_columns) - len(current_columns)
        if num_missing > 0:
            # Create a DataFrame with the missing columns, filled with NaN
            missing_cols = pd.DataFrame(
                np.nan, index=df.index, columns=expected_columns[len(current_columns):])
            # Concatenate the original DataFrame with the missing columns DataFrame
            df = pd.concat([df, missing_cols], axis=1)
        # Update the column names
        df.columns = expected_columns
    return df


df1 = ensure_columns(df1.iloc[:, 0:17], ['0', '1', '2', '3', '4',
                     '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'])
df2 = ensure_columns(df2.iloc[:, 0:17], ['0', '1', '2', '3', '4',
                     '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16'])
df3 = ensure_columns(df3.iloc[:, 0:16], ['0', '1', '2', '3', '4', '5',
                     '6', '7', '8', '9', '10', '11', '12', '13', '14', 'Unnamed: 15'])
df4 = ensure_columns(df4.iloc[:, 0:16], ['0', '1', '2', '3', '4',
                     '5', '6', '7', '8', '8.1', '10', '11', '12', '13', '14', '15'])
df5 = ensure_columns(df5.iloc[:, 0:10], [
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
df9 = ensure_columns(df9.iloc[:, 0:15], [
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'])


subset = df1[(df1["10"] != "Ja") & (df1["10"] != "Nej")]
superset = df1[(df1["10"] == "Ja") | (df1["10"] == "Nej")]
subset.insert(10, "Nothing", np.nan)
del subset["16"]

subset.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                  '13', '14', '15', '16']

df1_clean = pd.concat([superset, subset], ignore_index=True)

subset2 = df1_clean[(df1_clean["11"] == "Ja")]
superset2 = df1_clean[(df1_clean["11"] != "Ja")]

del subset2["11"]
# warnings.filterwarnings('ignore')
subset2.insert(16, "nothin", np.nan)

subset2.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                   '13', '14', '15', '16']

df1_clean = pd.concat([superset2, subset2], ignore_index=True)

del df1_clean["15"]
del df1_clean["16"]

df1_clean.columns = ["House_Name", "Location", "Slutpris", "Price_per_sqr_mtr", "Starting_price", "Price_Change",
                     "House_type", "Release_form", "Rooms", "Living_area", "Balcony", "Floor", "Built_on", "Charge", "Operating_cost"]

del df1_clean["Slutpris"]

subset3 = df2[(df2["11"] == "Ja")].copy()
superset3 = df2[(df2["11"] != "Ja")]

del subset3["11"]
subset3.loc[:, "nothing"] = np.nan


subset3.columns = superset3.columns

df2_clean = pd.concat([superset3, subset3], ignore_index=True)


subset4 = df2_clean[(df2_clean["13"].isna())]
superset4 = df2_clean[(df2_clean["13"].notna())]

subset4.insert(9, "Nothing", np.nan)

del subset4["16"]

subset4.columns = superset4.columns

df2_clean = pd.concat([superset4, subset4], ignore_index=True)


subset5 = df2_clean[(df2_clean["11"] == "Ja")]
superset5 = df2_clean[(df2_clean["11"] != "Ja")]

del subset5["11"]
# subset5["nothing"] = np.nan
subset5.loc[:, "nothing"] = np.nan

subset5.columns = superset5.columns

df2_clean = pd.concat([superset5, subset5], ignore_index=True)


del df2_clean["13"]
del df2_clean["14"]
del df2_clean["15"]
del df2_clean["16"]

df2_clean.columns = ["House_Name", "Location", "Slutpris", "Starting_price", "Price_Change", "House_type",
                     "Release_form", "Rooms", "Living_area", "Other_area", "Plot_area", "Built_on", "Operating_cost"]

del df2_clean["Slutpris"]

del df3["13"]
del df3["14"]
del df3["Unnamed: 15"]

df3.columns = ["House_Name", "Location", "Slutpris", "Starting_price", "Price_Change",
               "House_type", "Release_form", "Rooms", "Living_area", "Other_area", "Plot_area", "Built_on", "Operating_cost"]

del df3["Slutpris"]

del df4["15"]
del df4["14"]
del df4["13"]


df4.columns = ["House_Name", "Location", "Slutpris", "Starting_price", "Price_Change",
               "House_type", "Release_form", "Rooms", "Living_area", "Other_area", "Plot_area", "Built_on", "Operating_cost"]

del df4["Slutpris"]

del df5["8"]
del df5["9"]

df5.columns = ["House_Name", "Location", "Slutpris", "Starting_price", "Price_Change",
               "House_type", "Release_form", "Plot_area"]

del df5["Slutpris"]

del df9["13"]
del df9["14"]

df9.columns = ["House_Name", "Location", "Slutpris", "Starting_price", "Price_Change",
               "House_type", "Release_form", "Rooms", "Living_area", "Other_area", "Plot_area", "Built_on", "Operating_cost"]

del df9["Slutpris"]

df1_clean["Other_area"] = 0
df1_clean["Plot_area"] = 0

df2_clean["Price_per_sqr_mtr"] = np.nan
df2_clean["Charge"] = np.nan
df2_clean["Floor"] = np.nan
df2_clean["Balcony"] = np.nan

df3["Price_per_sqr_mtr"] = np.nan
df3["Charge"] = np.nan
df3["Floor"] = np.nan
df3["Balcony"] = np.nan


df4["Price_per_sqr_mtr"] = np.nan
df4["Charge"] = np.nan
df4["Floor"] = np.nan
df4["Balcony"] = np.nan

df5["Price_per_sqr_mtr"] = np.nan
df5["Charge"] = np.nan
df5["Floor"] = np.nan
df5["Balcony"] = np.nan
df5["Rooms"] = np.nan
df5["Living_area"] = np.nan
df5["Operating_cost"] = np.nan
df5["Other_area"] = np.nan
df5["Built_on"] = np.nan


df9["Price_per_sqr_mtr"] = np.nan
df9["Charge"] = np.nan
df9["Floor"] = np.nan
df9["Balcony"] = np.nan

order_columns = df1_clean.columns

df2_clean = df2_clean[order_columns]
df3 = df3[order_columns]
df4 = df4[order_columns]
df5 = df5[order_columns]
df9 = df9[order_columns]


df_combine = pd.concat(
    [df1_clean, df2_clean, df3, df4, df5, df9], ignore_index=True)

del df_combine["Price_per_sqr_mtr"]


df_combine["Sold_date"] = df_combine["Location"].str[-12:]

df_combine["Location"] = df_combine["Location"].str.split("-").str[1]

loc_list = df_combine["Location"].str.split(",").str[0]
df_combine["Location"] = df_combine["Location"].str.replace(" ", "")
df_combine["Municipality"] = df_combine["Location"].str.split(",").str[1]
df_combine["Municipality"] = df_combine["Municipality"].str[:-7]
df_combine["Municipality"] = df_combine["Municipality"].str.replace(" ", "")

df_combine["Location"] = loc_list


df_combine["Starting_price"] = df_combine["Starting_price"].str[:-2]

df_combine["Starting_price"] = df_combine["Starting_price"].str.replace(
    " ", "")

df_combine["Price_Change"] = df_combine["Price_Change"].str.split("kr").str[0]
df_combine["Price_Change"] = df_combine["Price_Change"].str.replace(" ", "")


# def convert_to_number(value):
#    try:
#        return int(value.replace('+', '').replace(',', ''))
#    except ValueError:
#        return np.nan


def convert_to_number(value):
    if isinstance(value, str):
        try:
            return int(value.replace('+', '').replace(',', ''))
        except ValueError:
            return np.nan
    else:
        return value


def convert_to_number_2(value):
    try:
        return float(value)
    except ValueError:
        return np.nan


df_combine["Price_Change"] = df_combine["Price_Change"].apply(
    convert_to_number)

df_combine["Starting_price"] = df_combine["Starting_price"].apply(
    convert_to_number)


df_combine["Rooms"] = df_combine["Rooms"].str[:-3]
df_combine["Rooms"] = df_combine["Rooms"].str.replace(",", ".")
df_combine["Rooms"] = df_combine["Rooms"].apply(convert_to_number_2)
df_combine.loc[df_combine["Rooms"] >= 19, "Rooms"] = 0

df_combine["Living_area"] = df_combine["Living_area"].str[:-
                                                          2].str.replace(",", ".")


df_combine["Living_area"] = df_combine["Living_area"].apply(
    convert_to_number_2)


part = df_combine["Floor"].str.split(",").str[0].str.split("av")
part2 = df_combine["Floor"].str.split(",").str[1]

df_combine["Lift"] = part2.str.strip().apply(
    lambda x: 'Yes' if x == 'hiss finns' else ('No' if x == 'hiss finns ej' else np.nan))

df_combine["Floor"] = part.str[0]

df_combine["Total_no_Floors"] = part.str[1]


df_combine_2 = df_combine.copy()  # Cache the cleaning of the data done until now


df_combine_2["Charge"] = df_combine_2["Charge"].str[:-6].str.replace(" ", "")
df_combine_2["Charge"] = df_combine_2["Charge"].apply(convert_to_number_2)

df_combine_2["Operating_cost"] = df_combine_2["Operating_cost"].str[:-
                                                                    5].str.replace(" ", "")
df_combine_2["Operating_cost"] = df_combine_2["Operating_cost"].apply(
    convert_to_number_2)

df_combine_2["Other_area"] = df_combine_2["Other_area"].str[:-
                                                            2].str.replace(",", ".")


df_combine_2["Other_area"] = df_combine_2["Other_area"].apply(
    convert_to_number_2)

# df_combine_2["Other_area"] = df_combine_2["Other_area"].fillna(
#   statistics.median(df_combine_2["Other_area"]))

df_combine_2["Plot_area"] = df_combine_2["Plot_area"].str[:-
                                                          2].str.replace(",", ".")


df_combine_2["Plot_area"] = df_combine_2["Plot_area"].apply(
    convert_to_number_2)

df_combine_2["Rooms"] = df_combine_2["Rooms"].fillna(0)


df_combine_2["Final_Price"] = df_combine_2["Starting_price"] - \
    df_combine_2["Price_Change"]


df_combine_2.loc[df_combine_2["Municipality"]
                 == "U", "Municipality"] = "Upplands-Bro"
df_combine_2.loc[df_combine_2["Municipality"] == "", "Municipality"] = np.nan

df_combine_2["House_type"] = df_combine_2["House_type"].str.replace(" ", "")
df_combine_2["Release_form"] = df_combine_2["Release_form"].str.replace(
    " ", "")

df_combine_2["Balcony"] = df_combine_2["Balcony"].str.replace(" ", "")
df_combine_2["Floor"] = df_combine_2["Floor"].str.replace(" ", "")
df_combine_2["Total_no_Floors"] = df_combine_2["Total_no_Floors"].str.replace(
    " ", "")
df_combine_2["Lift"] = df_combine_2["Lift"].str.replace(" ", "")


df_combine_2.loc[df_combine_2["Release_form"].isin(
    ["3 rum", "2 rum", "1 rum", "1,5 rum", "11 rum", "12 rum", "5 rum", "6 rum"]), "Release_form"] = np.nan


value_counts = df_combine_2["Floor"].value_counts()
values_to_replace = value_counts[value_counts <= 2].index
df_combine_2["Floor"] = df_combine_2["Floor"].replace(values_to_replace, 0)

# Replace specific values in "Floor" column
replace_values = ["1990", "2001", "-1", "2020", "2017", "1989", "10m²"]
df_combine_2["Floor"] = df_combine_2["Floor"].replace(replace_values, 0)

value_counts = df_combine_2["Total_no_Floors"].value_counts()
values = value_counts[value_counts == 1].index
df_combine_2["Total_no_Floors"] = df_combine_2["Total_no_Floors"].replace(
    values, 0)

df_combine_2["Total_no_Floors"] = df_combine_2["Total_no_Floors"].fillna(0)
df_combine_2["Floor"] = df_combine_2["Floor"].fillna(0)

df_combine_2["Balcony"] = df_combine_2["Balcony"].replace(np.nan, "Nej")

df_combine_2["House_type"] = df_combine_2["House_type"].replace(
    "Äganderätt", "Villa")
df_combine_2["House_type"] = df_combine_2["House_type"].replace(
    "Bostadsrätt", "Lägenhet")

value_counts = df_combine_2["Release_form"].value_counts()
values = value_counts[value_counts <= 6].index
df_combine_2["Release_form"] = df_combine_2["Release_form"].replace(
    values, "Bostadsrätt")


df_combine_2["Lift"] = df_combine_2["Lift"].fillna("No")

df_combine_2["Plot_area"] = df_combine_2["Plot_area"].fillna(
    df_combine_2["Plot_area"].median())
df_combine_2["Other_area"] = df_combine_2["Other_area"].fillna(
    df_combine_2["Other_area"].median())
df_combine_2["Living_area"] = df_combine_2["Living_area"].fillna(
    df_combine_2["Living_area"].median())
df_combine_2["Charge"] = df_combine_2["Charge"].fillna(
    df_combine_2["Charge"].median())
df_combine_2["Operating_cost"] = df_combine_2["Operating_cost"].fillna(
    df_combine_2["Operating_cost"].median())

replacements = {'Nej': 'No', 'Ja': 'Yes'}

df_combine_2["Balcony"] = df_combine_2["Balcony"].replace(replacements)


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')


# def parse_date(date_str):
#    date_str = date_str.strip()
#    return datetime.strptime(date_str, '%d %B %Y')


def parse_date(date_str):
    if isinstance(date_str, str):
        date_str = date_str.strip()  # Strip any leading/trailing whitespace
    return date_str


df_combine_2['Sold_date'] = df_combine_2['Sold_date'].apply(parse_date)

df_combine_2["Location"] = df_combine_2["Location"].str.replace(" ", "")
df_combine_2['Location'] = df_combine_2.Location.astype('category')

df_combine_2['House_type'] = df_combine_2.House_type.astype('category')
df_combine_2['Release_form'] = df_combine_2.Release_form.astype('category')
df_combine_2['Rooms'] = df_combine_2.Rooms.astype('int')
df_combine_2['Balcony'] = df_combine_2.Balcony.astype('category')
df_combine_2['Floor'] = df_combine_2.Floor.astype('int')
df_combine_2["Built_on"] = df_combine_2["Built_on"].apply(convert_to_number_2)

df_combine_2["Built_on"] = df_combine_2["Built_on"].fillna(
    statistics.median(df_combine_2["Built_on"]))
df_combine_2['Municipality'] = df_combine_2.Municipality.astype('category')
df_combine_2['Lift'] = df_combine_2.Lift.astype('category')
df_combine_2['Total_no_Floors'] = df_combine_2.Total_no_Floors.astype(
    'int')


df_combine_2 = df_combine_2[["House_Name", "Location", "Municipality", "House_type", "Release_form", "Rooms", "Floor", "Total_no_Floors", "Lift", "Balcony",
                             "Living_area", "Plot_area", "Other_area", "Built_on", "Charge", "Operating_cost", "Sold_date", "Starting_price", "Price_Change", "Final_Price"]]


df_combine_2["Starting_price"] = df_combine_2["Starting_price"]/1000000
df_combine_2["Price_Change"] = df_combine_2["Price_Change"]/1000000
df_combine_2["Final_Price"] = df_combine_2["Final_Price"]/1000000

df_combine_2 = df_combine_2.dropna(subset=['Starting_price'])


df_combine_2 = df_combine_2.reset_index(drop=True)

df_combine_2["Built_on"] = df_combine_2["Built_on"].astype(object)

for i in range(df_combine_2.shape[0]):
    if df_combine_2["Built_on"].iloc[i] < 1900:
        df_combine_2.loc[i, "Built_on"] = "Before 1900s"
    elif df_combine_2["Built_on"].iloc[i] >= 1900 and df_combine_2["Built_on"].iloc[i] <= 1950:
        df_combine_2.loc[i, "Built_on"] = "1900-1950"
    elif df_combine_2["Built_on"].iloc[i] >= 1951 and df_combine_2["Built_on"].iloc[i] <= 2000:
        df_combine_2.loc[i, "Built_on"] = "1951-2000"
    elif df_combine_2["Built_on"].iloc[i] >= 2001 and df_combine_2["Built_on"].iloc[i] <= 2010:
        df_combine_2.loc[i, "Built_on"] = "2001-2010"
    elif df_combine_2["Built_on"].iloc[i] >= 2011 and df_combine_2["Built_on"].iloc[i] <= 2030:
        df_combine_2.loc[i, "Built_on"] = "2011-present"


df_combine_2['Sold_date'] = pd.to_datetime(
    df_combine_2['Sold_date'], format='%d %B %Y').dt.strftime('%Y-%m-%d')


# df_combine_2 = df_combine_2.dropna(subset=['Municipality'])
df_combine_2 = df_combine_2.dropna()

df_combine_2.loc[df_combine_2['House_type'] ==
                 'Lägenhet', ['Plot_area', 'Other_area']] = 0


df_combine_2.to_csv("data.csv")

db = mysql.connector.connect(
    user="siddhesh",
    password="Zxcvbnm1234",
    # Kept the credientials open to the public for now due to restriction issues when using github secerts for MySQL. But the database is still secure since the below
    # inputs are kept secret.
    host="database101.mysql.database.azure.com",
    port=3306,
    database="sweden_property"
)

cursor = db.cursor()

rows = [tuple(row) for row in df_combine_2.values]


sql = """
    INSERT INTO housing_prices (House_Name, Location, Municipality, House_type, Release_form,
                            Rooms, Floor, Total_no_Floors, Lift, Balcony, Living_area,
                            Plot_area, Other_area, Built_on, Charge, Operating_cost,
                            Sold_date, Starting_price, Price_Change, Final_Price)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

cursor.executemany(sql, rows)


db.commit()
cursor.close()
db.close()
