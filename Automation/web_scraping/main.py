import requests
import pandas as pd
import time
from selenium import webdriver
import pyautogui
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class Data:
    def __init__(self, place, yesterday, today):
        self.place = place
        self.yesterday = yesterday
        self.today = today

class Item:
    def __init__(self, name):
        self.name = name
        self.wholesale = []
        self.retail = []


sampele_url = 'https://www.cbsl.gov.lk/sites/default/files/cbslweb_documents/statistics/pricerpt/price_report_20250508_e.pdf'
web_url = 'https://smallpdf.com/pdf-to-excel#r=convert-to-excel'

def download_pdf(url):
    """
    Download a PDF file from a given URL and save it to a local file.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with open('sample.pdf', 'wb') as f:
            f.write(response.content)
        print("PDF downloaded successfully.")
    else:
        print("Failed to download PDF.")

def automated_pdf_to_xslx():
    global web_url
    webdriver_path = 'chromedriver.exe'
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service)
    driver.get(web_url)
    time.sleep(5)  # Wait for the page to load

    # click on /html/body/div[1]/div/div[1]/header/div[2]/div/div/div/div/div/div[3]/div[2]/div[2]/div/div[2]/form/label/div/div[1]/div[2]/div/button[1]
    driver.find_element("xpath", "/html/body/div[1]/div/div[1]/header/div[2]/div/div/div/div/div/div[3]/div[2]/div[2]/div/div[2]/form/label/div/div[1]/div[2]/div/button[1]").click()
    time.sleep(5)  # Wait for open the upload file dialog

    # upload the file
    pyautogui.write('C:\\Users\\SAHAN\\Dark\\personal\\Automation\\web_scraping\\sample.pdf')
    pyautogui.press('enter')
    time.sleep(20)  # Wait for the file to be uploaded

    # click on /html/body/div[1]/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]/button[2]
    driver.find_element("xpath", "/html/body/div[1]/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]/button[2]").click()
    time.sleep(20)  # Wait for the file to be converted
    
    # click on /html/body/div[1]/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/a
    driver.find_element("xpath", "/html/body/div[1]/div/div/div[3]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/a").click()
    time.sleep(20)  # Wait for the file to be downloaded

    # close the browser
    driver.quit()
    print("PDF converted to CSV successfully.")

def read_xlsx_file(file_path):
    """
    Read an Excel file and return the data as a pandas DataFrame.
    """
    try:
        df = pd.read_excel(file_path)
        print("Excel file read successfully.")
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None
    
def make_data_models(df):
    """
    Create data models from the DataFrame.
    """
    data_models = {}
    df = df[4:-3] # Get item names from the first row
    cat = ["VEGETABLES", "OTHER", "FRUITS", "RICE", "FISH"]
    current_cat = ""

    for i in range(0, df.shape[0]):
        if df.iloc[i, 0] == "" or pd.isnull(df.iloc[i, 0]): # Skip empty rows
            continue
        name = df.iloc[i,0]
        if  name.replace(" ","") in cat:
            data_models.update({name.replace(" ",""): []})
            current_cat = name.replace(" ","")
        else:
            item = Item(name)
            item.retail.append(Data("Narahenpita", df.iloc[i, 10], df.iloc[i, 11]))
            if current_cat == "RICE":
                item.wholesale.append(Data("Marandagahamula", df.iloc[i, 4], df.iloc[i, 5]))
            elif current_cat == "FISH":
                item.wholesale.append(Data("Negombo", df.iloc[i, 4], df.iloc[i, 5]))
            else:
                item.wholesale.append(Data("Dambulla", df.iloc[i, 4], df.iloc[i, 5]))
            if current_cat == "FISH":
                item.wholesale.append(Data("Peliyagoda", df.iloc[i, 2], df.iloc[i, 3]))
                item.retail.append(Data("Negombo", df.iloc[i, 8], df.iloc[i, 9]))
            else:
                item.wholesale.append(Data("Pettah", df.iloc[i, 2], df.iloc[i, 3]))
                item.retail.append(Data("Pettah", df.iloc[i, 6], df.iloc[i, 7]))
                item.retail.append(Data("Dambulla", df.iloc[i, 8], df.iloc[i, 9]))
            data_models[current_cat].append(item)
    return data_models
def main():
    # Download the PDF file
    download_pdf(sampele_url)

    # Convert the PDF to CSV
    automated_pdf_to_xslx()

    # Read the XSLX file
    # Read the second sheet named "Table 2" from the Excel file
    df = pd.read_excel('C:\\Users\\SAHAN\\Downloads\\sample.xlsx', sheet_name='Table 2')
    # print(df)  # Print the first 5 rows of the dataframe

    if df is not None:
        # Create data models
        data_models = make_data_models(df)
        # Print the data models
        for cat, items in data_models.items():
            print(f"{cat}:")
            for item in items:
                print(f"  {item.name}:")
                print(f"    Wholesale: {[f'{data.place}: {data.yesterday} - {data.today}' for data in item.wholesale]}")
                print(f"    Retail: {[f'{data.place}: {data.yesterday} - {data.today}' for data in item.retail]}")
    else:
        print("Failed to read Excel file.")

if __name__ == "__main__":
    main()