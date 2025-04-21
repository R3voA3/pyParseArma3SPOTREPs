# Loops through all .html files in the output folder
# and parses them to be used on the BIKI
# The output is saved in the wiki.wiki file

from bs4 import BeautifulSoup as bs
from pathlib import Path
import os, glob

def getTitleFromFileName(fileName):
    return fileName.removesuffix('.html')

def buildURL(title):
    return r'https://dev.arma3.com/post/' + title.lower()

def buildURLWiki(url, title):
    return r'{{Link|' + url + '|' + title + r'}}'

def ignoreTAG(line):
    ignoreTAGs = [
        '<div class="post-content">',
        '</p>',
        '<p>',
        '<div>',
        '</div>',
        '<p class="text-bold">',
        '<i>',
        '</i>',
        '<br>',
        '</br>',
        '<br/>',
        '</em>',
        '<em>',
        '<ul>',
        '</ul>',
        '<span>',
        '</span>',
        '</h2>',
        '</h1>',
        '<b>'
    ]

    for tag in ignoreTAGs:
        if (tag in line):
            return True
    return False

def parseHTMLFiles():
    pathWiki = r'output\\wiki.wiki'

    targetFile = open(pathWiki, 'w+', encoding='utf-8')

    # Get all source files
    path = os.path.join('output', '*.html')

    # Sort the files because first two spotreps have diff. name
    files = sorted(glob.glob(path), key=os.path.getctime)

    linesFormatted = []

    index = 0

    for sourceFile in files:
        sourceFile = open(sourceFile, 'r', encoding='utf-8')

        title = getTitleFromFileName(os.path.basename(sourceFile.name))
        sectionTitle = f'== {title} =='
        url = buildURL(title)
        wikiLink = buildURLWiki(url, title)

        # Add beginning of each SPOTREP
        if index > 0:
            linesFormatted.append('\n\n')

        linesFormatted.append(sectionTitle)
        linesFormatted.append('\n\n')
        linesFormatted.append(wikiLink)
        linesFormatted.append('\n\n')

        # soup = bs(sourceFile, 'html.parser')
        # paragraph = soup.p.get_text('\n\n', True)

        # targetFile.write(paragraph)

        # headlines = soup.find_all("h1")

        # for headline in headlines:
        #     targetFile.write("\n\n")
        #     targetFile.write(f"=== {headline.get_text().strip()} ===")
        #     targetFile.write("\n")

        # firstHeadline = soup.find("h1")

        # if (index == 0):
        #     for child in soup.find_all():
        #         print(child.contents)
        #         print("------------")

        lines = sourceFile.readlines()
        liCount = 0
        h1 = False
        h2 = False
        strong = False
        boxInNextLine = False

        for line in lines:
            line = line.lstrip()
            lineFormatted = line.lstrip()

            if (liCount == 1):
                lineFormatted = "* " + lineFormatted

            if (liCount == 2):
                lineFormatted = "** " + lineFormatted

            if (strong):
                lineFormatted = f"* '''{line.rstrip()}'''\n"
                strong = False

            if (h1):
                lineFormatted = f"\n=== {line.rstrip()} ===\n"
                h1 = False

            if (h2):
                lineFormatted = f"\n==== {line.rstrip()} ====\n\n"
                h2 = False

            if (boxInNextLine):
                lineFormatted = f"\n==== {line.rstrip()} ====\n\n"
                boxInNextLine = False

            if (line.startswith("FROM:") or
                line.startswith("TO:") or
                line.startswith("UNIT:") or
                line.startswith("ACTIVITY:") or
                line.startswith("SIZE:")):
                lineFormatted = "* " + line

            if (ignoreTAG(line)):
                continue

            if (line.startswith(r'-mod')):
                lineFormatted = r"'''" + line.strip() + r"'''"

            if (line.startswith(r'<li>')):
                liCount += 1
                continue

            if (line.startswith(r'</li>')):
                liCount -= 1
                continue

            if (line.startswith(r'<h1>')):
                h1 = True
                continue

            if (line.startswith(r"<h2>")):
                h2 = True
                continue

            if (line.startswith(r'<strong>') or
                line.startswith(r'<b>')):
                strongCount = True
                continue

            if (line.startswith(r'<h2 class="box_title">')):
                boxInNextLine = True
                continue

            linesFormatted.append(lineFormatted)
            # targetFile.write(lineFormatted)

        sourceFile.close()

        index = index =+ 1
    targetFile.writelines(linesFormatted)
    targetFile.close()

if __name__ == '__main__':
    parseHTMLFiles()