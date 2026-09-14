import json
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# e.g., https://www.google.com
BASE_URL = "Your website base url"


def create_driver():
    options = Options()

    # Enable Chrome performance/network logs
    options.set_capability(
        "goog:loggingPrefs",
        {"performance": "ALL"}
    )

    driver = webdriver.Chrome(options=options)
    return driver


def login(driver):
    driver.get(BASE_URL)
    input("Perform login then press enter")


def get_browser_cookies(driver):
    cookies = driver.get_cookies()

    return {
        cookie["name"]: cookie["value"]
        for cookie in cookies
    }


def get_network_headers(driver, url_contains):
    """
    Get request headers from Chrome performance logs
    for a request whose URL contains url_contains.
    """

    logs = driver.get_log("performance")

    for entry in logs:
        message = json.loads(entry["message"])["message"]

        if message["method"] != "Network.requestWillBeSent":
            continue

        request = message["params"]["request"]
        url = request["url"]

        if url_contains in url:
            return request["headers"]

    return {}


def create_api_session(driver):
    session = requests.Session()

    # Copy browser cookies
    for cookie in driver.get_cookies():
        session.cookies.set(
            cookie["name"],
            cookie["value"],
            domain=cookie.get("domain"),
            path=cookie.get("path", "/")
        )

    return session


class ApiClient:

    # e.g., https://api.google.com
    BASE = "your api base url"

    def __init__(self, driver):
        self.session = requests.Session()

        for cookie in driver.get_cookies():
            self.session.cookies.set(
                cookie["name"],
                cookie["value"]
            )

    def get(self, endpoint, **kwargs):
        return self.session.get(
            self.BASE + endpoint,
            **kwargs
        )

    def post(self, endpoint, **kwargs):
        return self.session.post(
            self.BASE + endpoint,
            **kwargs
        )


def main():
    driver = create_driver()

    login(driver)

    api = TiketApiClient(driver)

    response = api.get(
        "your endpoint"
    )

    assert response.status_code == 200
    print(response.text)

    driver.quit()

if __name__ == "__main__":
    main()
