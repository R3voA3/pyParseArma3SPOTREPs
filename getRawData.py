# Gets all changelogs from the BI website and stores
# each changelog in its own file

from bs4 import BeautifulSoup
import requests
import time

pathRawData = r"output\rawHTML.txt"
startPageIndex = 1
endPageIndex = 118
intervalPerPage = 0.1

def buildSPOTREPName(i):
    if i < 3:
        # The first two SPOTREPs have a different number of leading zeros than the rest.
        return f"spotrep-00{i:02d}"
    else:
        return f"spotrep-00{i:03d}"

def getRawDataFromWeb():
    indices = range(startPageIndex, endPageIndex)

    for i in indices:
        SPOTREPName = buildSPOTREPName(i)
        url = f"https://dev.arma3.com/post/{SPOTREPName}"
        file = open(f"output\\{SPOTREPName.upper()}.html" ,"w+", encoding="utf-8")

        print(f"Fetching {url}")

        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML and find the changelog:
            soup = BeautifulSoup(response.text, "html.parser")
            changelog = soup.find("div", class_ = "post-content")

            file.writelines(changelog.prettify())
        else:
            raise Exception(f"Received unexpected response status code {response.status_code} for {url}")

        time.sleep(intervalPerPage) # Avoid flooding the server with requests
        file.close()


if __name__ == '__main__':
    getRawDataFromWeb()