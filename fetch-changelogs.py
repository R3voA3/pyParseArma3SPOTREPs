#
# Fetches Arma 3 changelogs.
#
# Dependencies:
#	beautifulsoup4
# 	requests
#

from bs4 import BeautifulSoup
import requests
import time
import re

def indexToUrl(i):
    if i < 3:
        return f"https://dev.arma3.com/post/spotrep-00{i:02d}" # The first two SPOTREPs have a different number of leading zeros than the rest.
    else:
        return f"https://dev.arma3.com/post/spotrep-00{i:03d}"

indices = range(1, 118) # The latest SPOTREP is #00117.
sourceFile = open(r"D:\Changelog.txt","w+", encoding="utf-8")

for i in indices:
    url = indexToUrl(i)

    print(f"Fetching {url}")

    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML and find the changelog:
        soup = BeautifulSoup(response.text, "html.parser")
        changelog = soup.find("div", class_ = "post-content")

        # Format title and add link to official page
        spotrepTitle = url.split(r"/")[-1].upper()
        spotrepTitle = f"== {spotrepTitle} ==\n\n" + r"{{Link|" + f"{url}|{spotrepTitle}" + r"}}" + "\n"
        sourceFile.write(spotrepTitle)

        content = changelog.prettify()

        sourceFile.writelines(content)
    else:
        raise Exception(f"Received unexpected response status code {response.status_code} for {url}")

    time.sleep(0.1) # Avoid flooding the server with requests.

# Format sourceFile
sourceFile = open(r"D:\Changelog.txt","r", encoding="utf-8")
targetFile = open(r"D:\ChangelogBikiFOrmat.txt","w+", encoding="utf-8")

lines = sourceFile.readlines()

ulStartCount = 0
liStartCount = 0
h1StartCount = 0
h2StartCount = 0
strongCount = 0
emCount = 0
boxInNextLine = False

for line in lines:
    print(liStartCount)

    line = line.lstrip()
    lineFormatted = line.lstrip()

    if (liStartCount == 1):
        lineFormatted = "* " + lineFormatted

    if (liStartCount == 2):
        lineFormatted = "** " + lineFormatted

    if (strongCount == 1):
        lineFormatted = f"* '''{line.rstrip()}'''\n"

    # if (emCount == 1):
    #     # lineFormatted = f"* ''{line.rstrip()}''\n"
    #     continue

    if (h1StartCount == 1):
        lineFormatted = f"\n=== {line.rstrip()} ===\n"

    if (h2StartCount == 1):
        lineFormatted = f"\n==== {line.rstrip()} ====\n\n"

    if (boxInNextLine):
        lineFormatted = f"\n==== {line.rstrip()} ====\n\n"
        boxInNextLine = False

    if (line.startswith("FROM:") or
        line.startswith("TO:") or
        line.startswith("UNIT:") or
        line.startswith("ACTIVITY:") or
        line.startswith("SIZE:")):
        lineFormatted = "* " + line

    if (line.startswith(r"<br>") or
        line.startswith(r"</br>") or
        line.startswith(r"<br/>")):
        # lineFormatted = "\n"
        continue

    if (line.startswith(r'<div class="post-content">') or
        line.startswith(r"</p>") or
        line.startswith(r"<p>") or
        line.startswith(r"<div>") or
        line.startswith(r"</div>")):
        continue

    if (line.startswith(r"<li>")):
        liStartCount += 1
        continue

    if (line.startswith(r"</li>")):
        liStartCount -= 1
        continue

    if (line.startswith(r"<ul>")):
        ulStartCount += 1
        continue

    if (line.startswith(r"</ul>")):
        ulStartCount -= 1
        continue

    if (line.startswith(r"<h1>")):
        h1StartCount += 1
        continue

    if (line.startswith(r"</h1>")):
        h1StartCount -= 1
        continue

    if (line.startswith(r"<h2>")):
        h2StartCount += 1
        continue

    if (line.startswith(r"</h2>")):
        h2StartCount -= 1
        continue

    if (line.startswith(r"<strong>")):
        strongCount += 1
        continue

    if (line.startswith(r"</strong>")):
        strongCount -= 1
        continue

    if (line.startswith(r"<em>")):
        # emCount += 1
        continue

    if (line.startswith(r"</em>")):
        # emCount -= 1
        continue

    if (line.startswith(r'<h2 class="box_title">')):
        boxInNextLine = True
        continue

    print(lineFormatted)
    targetFile.write(lineFormatted)

sourceFile.close()
targetFile.close()