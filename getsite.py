import sys
from bs4 import BeautifulSoup
import requests

# Get text content from URL
def getText(url="https://www.oaktreeanimals.org.uk/", Print=False):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    siteText = soup.get_text(strip=False)
    if Print:
        print(siteText)
    return siteText

# Update list of pages for AI to read
def updatePages(operation, url, pages_file):
    with open(pages_file, 'r') as f:
        pages = f.read().splitlines()

    if operation == 'add':
        if url not in pages:
            pages.append(url)
            print(f"Added {url} to the list of pages.")
        else:
            print(f"{url} is already in the list of pages.")
    elif operation == 'rm':
        if url in pages:
            pages.remove(url)
            print(f"Removed {url} from the list of pages.")
        else:
            print(f"{url} is not in the list of pages.")
    else:
        print("Invalid operation. Use 'add' or 'rm'.")

    with open(pages_file, 'w') as f:
        for page in pages:
            f.write(page + '\n')

pages_file = "pages.txt"


if __name__ == "__main__":

    # Check if command-line arguments are provided for adding or removing a URL
    if len(sys.argv) >= 3:
        operation = sys.argv[1]
        url = sys.argv[2]
        updatePages(operation, url, pages_file)

    # Splitlines is more memory efficient than readlines
    with open(pages_file, 'r') as f:
        pages = f.read().splitlines()

    # Write the text content of the pages to website.txt
    with open("website.txt", "w", encoding="utf-8") as f:
        for page in pages:
            text_content = getText(url=page)
            f.write(text_content)
