import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

# AWS S3 configuration
# set up your keys in your enviornment file
aws_auth = {
        "aws_access_key_id" : os.environ.get("aws_access_key_id"),
        "aws_secret_access_key" : os.environ.get("aws_secret_access_key"),
        "region_name" : os.environ.get("region")
    }

BUCKET_NAME = #your bucket name
FOLDER_NAME = #folder name

# Initialize S3 client
try:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_auth["aws_access_key_id"],
        aws_secret_access_key=aws_auth["aws_secret_access_key"],
        region_name=aws_auth["region_name"]
    )
    print("Successfully connected to S3")
except NoCredentialsError:
    print("AWS credentials not available")
except ClientError as e:
    print(f"Failed to connect to S3: {e}")

# Function to download a file
def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Downloaded {filename}")

# Function to upload a file to S3
def upload_to_s3(filename, bucket, folder):
    try:
        s3_client.upload_file(filename, bucket, folder + filename)
        print(f"Uploaded {filename} to s3://{bucket}/{folder + filename}")
    except FileNotFoundError:
        print(f"The file {filename} was not found")
    except NoCredentialsError:
        print("Credentials not available")
    except ClientError as e:
        print(f"Failed to upload {filename} to S3: {e}")

# Function to check if the publication is in English and not a Form or Notice
def is_valid_document(filename):
    if filename[0].lower() in ['n', 'f']:
        return False
    if not filename.rstrip('.pdf')[-1].isdigit():
        return False
    return True

# Initialize Selenium WebDriver with Firefox
firefox_options = Options()
firefox_options.add_argument("--headless")  # Run in headless mode
service = Service('/usr/local/bin/geckodriver')  # Specify path to geckodriver
driver = webdriver.Firefox(service=service, options=firefox_options)

# URL of the IRS forms and publications page
# Change URL if needed
base_url = "https://www.irs.gov/forms-instructions-and-publications"
driver.get(base_url)
time.sleep(5)  # Increase wait time to ensure the page is fully loaded

# Counter for the total number of documents downloaded
total_downloaded = 0
download_limit = 3000  # Limit amount of documents

# Set to track downloaded files and avoid duplication
downloaded_files = set()

# Loop through all pages
while total_downloaded < download_limit:
    print(f"Scraping page: {driver.current_url}")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a', href=True)
    pdf_links = [link for link in links if link['href'].endswith('.pdf')]

    download_count = 0

    for link in pdf_links:
        if download_count >= download_limit:
            break

        filename = link['href'].split('/')[-1]
        if is_valid_document(filename) and filename not in downloaded_files:
            pdf_url = link['href']
            if not pdf_url.startswith("https://"):
                pdf_url = "https://www.irs.gov" + pdf_url
            print(f"Downloading {filename} from {pdf_url}")
            download_file(pdf_url, filename)
            upload_to_s3(filename, BUCKET_NAME, FOLDER_NAME)
            os.remove(filename)  # Remove the file after uploading to S3
            download_count += 1
            downloaded_files.add(filename)

    total_downloaded += download_count

    # Attempt to find and click the "Next" button using more specific selectors
    try:
        next_button = driver.find_element(By.XPATH, "//a[@title='Go to next page']")
        print("Found 'Next' button using XPATH")
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(5)  # Wait for the AJAX request to complete and the new page to load
    except Exception as e:
        print(f"No 'Next' button found or error occurred: {e}")
        break

driver.quit()
print("Download and upload complete.")
