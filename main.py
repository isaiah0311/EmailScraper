import requests
import re
import bs4
import urllib

def scrape_links(response: requests.Response, base: str):
    """Scrapes a webpage for links to other pages.

    Args:
        response (requests.Response): Response to the GET request
        base (str): URL base
    
    Returns:
        list: List of links found
    """
    collected = []

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    anchors = soup.find_all("a")
    for anchor in anchors:
        href = anchor.get("href")
        if href != None:
            link = ""
            if href[0] == "#":
                continue
            elif "http://" in href or "https://" in href:
                link = href
            else:
                link = base + href

            if collected.count(link) == 0:
                collected.append(link)
    
    return collected

def scrape_emails(response: requests.Response):
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

def request_url(url: str):
    """Sends a GET request to the target.

    Args:
        url (str): URL to send the GET request to
    
    Returns:
        list: List of email addresses found
        list: List of links found
        bool: Whether or not the script should exit
    """
    emails = []
    links = []
    quit = False

    parts = urllib.parse.urlsplit(url)
    base = "{0.scheme}://{0.netloc}".format(parts)

    try:
        response = requests.get(url)
        response.raise_for_status()

        emails = scrape_emails(response)
        links = scrape_links(response, base)
    except KeyboardInterrupt:
        quit = True
    except:
        print("ERROR: " + url)
    else:
        print(url)
    
    return emails, links, quit

def main():
    """Entry point for the script."""
    results = []

    target = input("Enter target: ")

    queue = [target]
    done = []

    for url in queue:
        emails, links, quit = request_url(queue[0])

        for email in emails:
            if results.count(email) == 0:
                results.append(email)
        
        for link in links:
            if queue.count(link) == 0 and done.count(link) == 0:
                queue.append(link)

        queue.pop(0)
        done.append(url)

        if quit:
            break

    print()
    for email in results:
        print(email)

if __name__ == "__main__":
    main()
