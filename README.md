# IRS Forms and Publications Scraper

## Overview

This project is a web scraping tool designed to automate the process of downloading PDF documents from the IRS Forms and Publications page and uploading them to an AWS S3 bucket. The tool uses Selenium with the Firefox WebDriver to navigate through multiple pages on the IRS website, downloads the PDF files, checks for certain criteria, and then uploads the valid files to a specified S3 bucket.

## Prerequisites

Before running the script, ensure you have the following installed:

- Python 3.x
- Selenium
- BeautifulSoup4
- Boto3
- Geckodriver (for Firefox WebDriver)
- Firefox browser

### Python Libraries

Install the required Python libraries using `pip`:

```bash
pip install selenium beautifulsoup4 boto3 requests
```

### Geckodriver

Download and install Geckodriver to allow Selenium to control the Firefox browser. Ensure that the Geckodriver is added to your system's PATH or specify its location in the script.

## Configuration

### AWS Configuration

You need to set up your AWS credentials and region in your environment. These credentials should have the necessary permissions to upload files to the specified S3 bucket.

1. Set your AWS credentials and region in your environment variables:

```bash
export aws_access_key_id=YOUR_AWS_ACCESS_KEY_ID
export aws_secret_access_key=YOUR_AWS_SECRET_ACCESS_KEY
export region=YOUR_AWS_REGION
```

2. Set the following variables in the script:

- `BUCKET_NAME`: The name of your S3 bucket.
- `FOLDER_NAME`: The folder in your S3 bucket where the files will be uploaded.

### Selenium WebDriver

Ensure the path to Geckodriver is correct in the script:

```python
service = Service('/usr/local/bin/geckodriver')  # Update this path if needed
```

## How to Use

1. **Run the Script:**

   Execute the script using Python:

   ```bash
   python scraper.py
   ```

   The script will start by navigating to the IRS Forms and Publications page and downloading PDF files that meet the specified criteria. The files are then uploaded to the specified S3 bucket.

2. **Download and Upload Process:**

   - The script checks if a PDF file is valid based on its filename (it avoids forms and notices by skipping filenames starting with 'n' or 'f').
   - Files are downloaded and uploaded to S3.
   - After uploading, the local copy of the file is deleted to save space.

3. **Pagination Handling:**

   - The script attempts to click the "Next" button to move through the pages and continue downloading files until the specified limit is reached or no more pages are available.

4. **Completion:**

   Once the script finishes, it will close the browser and print a completion message.

## Error Handling

- The script includes basic error handling for issues such as missing AWS credentials, failure to connect to S3, and missing files.
- If the script encounters an issue with locating the "Next" button or an error while clicking it, it will stop the scraping process.

## Customization

- **Download Limit:** You can change the `download_limit` variable to set how many files you want to download.
- **File Validation:** Modify the `is_valid_document` function to change the criteria for which files are downloaded.

## Notes

- The script runs in headless mode by default, meaning that the Firefox browser will not open visually. This can be changed by removing the headless argument if you wish to see the browser.

- Ensure that your AWS S3 bucket has the appropriate permissions to allow the upload of files from this script.

## Disclaimer

This tool is intended for educational and research purposes. Be sure to comply with the IRS website's terms of use and respect any scraping guidelines they may have.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.