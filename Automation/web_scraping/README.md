# README

## Project Overview

This project is a Python application.

## Project Structure

The project structure is as follows:

```
- chromedriver.exe
- main.py
- sample.pdf
```

## Project Details

This project contains the following files:

- main.py
### main.py
This Python code automates the process of extracting price data from a PDF report published by the Central Bank of Sri Lanka, converting it into a structured data format, and then printing the extracted data. Here's a breakdown:

1.  **Imports Libraries:** Imports necessary libraries such as `requests` for downloading files, `pandas` for data manipulation, `time` for pausing execution, `selenium` for web automation, and `pyautogui` for UI automation.

2.  **Data Structures:** Defines two classes:
    *   `Data`:  Represents price information for a specific place, containing yesterday's and today's prices.
    *   `Item`:  Represents a specific item, storing its name and lists of wholesale and retail price data (`Data` objects).

3.  **Download PDF:** The `download_pdf` function downloads the PDF report from a given URL.

4.  **Automated PDF to XLSX Conversion:** The `automated_pdf_to_xslx` function uses Selenium and PyAutoGUI to automate the following steps:
    *   Opens the `smallpdf.com` website for PDF to Excel conversion.
    *   Uploads the downloaded PDF file.
    *   Converts the PDF to Excel format.
    *   Downloads the resulting XLSX file.
    *   Closes the browser.

5.  **Read XLSX File:** The `read_xlsx_file` function reads the downloaded XLSX file into a pandas DataFrame.

6.  **Make Data Models:** The `make_data_models` function:
    *   Takes the DataFrame as input.
    *   Iterates through the rows of the DataFrame.
    *   Identifies category headers (`VEGETABLES`, `OTHER`, `FRUITS`, `RICE`, `FISH`).
    *   Extracts item names, wholesale prices, and retail prices from the DataFrame.
    *   Creates `Item` and `Data` objects to represent the extracted data.
    *   Organizes the data into a dictionary called `data_models` with categories as keys and lists of `Item` objects as values.

7.  **Main Function:**
    *   Calls `download_pdf` to download the PDF.
    *   Calls `automated_pdf_to_xslx` to convert the PDF to XLSX using web automation.
    *   Reads the "Table 2" sheet of the downloaded Excel file using pandas.
    *   Calls `make_data_models` to structure the data from the pandas DataFrame into the defined `Item` and `Data` classes.
    *   Iterates through the `data_models` dictionary and prints the extracted data in a user-friendly format, including item names, wholesale prices with locations, and retail prices with locations.

In essence, the code automates a data extraction and structuring pipeline. It fetches a PDF report, converts it to a more easily processed format (XLSX), extracts the relevant price data, and then presents the data in a structured and readable way.  It leverages external tools (like smallpdf.com) for the conversion, using Selenium and PyAutoGUI to handle the website interactions.


