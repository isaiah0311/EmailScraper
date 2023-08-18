import requests
import re

def scrapeWebpage(response: requests.Response):
    """Scrapes a webpage for email addresses.

    Args:
        response (requests.Response): Response to the GET request
    
    Returns:
        list: List of email addressed found
    """
    collected = []

    emails = re.findall(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",\
                        response.text)
    for email in emails:
        if collected.count(email) == 0:
            collected.append(email)
    
    return collected

def requestURL(url: str):
    """Sends a GET request to the target.

    Args:
        url (str): URL to send the GET request to
    
    Returns:
        list: List of email addresses found
    """
    emails = []

    try:
        response = requests.get(url)
        response.raise_for_status()
        emails = scrapeWebpage(response)
    except Exception as exception:
        print(exception)
    
    return emails

def main():
    """Entry point for the script."""
    url = input("Enter target: ")
    emails = requestURL(url)
    for email in emails:
        print(email)

if __name__ == "__main__":
    main()
