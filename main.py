import requests

def requestURL(url: str):
    """Sends a GET request to the target.

    Args:
        url (str): URL to send the GET request to
    """

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as exception:
        print(exception)
    else:
        print("Success")

def main():
    """Entry point for the script."""
    url = input("Enter target: ")
    requestURL(url)


if __name__ == "__main__":
    main()
