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

def replaceStuffInOutputFile(content):
    test = r'In case of problems, please check the \
   <a href="http://support.bistudio.com/arma-3" target=""> \
    Bohemia Interactive support F.A.Q.'

    content = content.replace(test, 'blabla')

    return content

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
        '</b>',
        '</strong>'
    ]

    for tag in ignoreTAGs:
        if (tag in line):
            return True
    return False

def parseHTMLFiles():
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

        lines = sourceFile.readlines()
        liCount = 0
        h1 = False
        h2 = False
        strong = False
        boxInNextLine = False
        isInsideHref = False

        for line in lines:
            line = line.lstrip()
            lineFormatted = line.lstrip()

            # href detection
            # anything between <href> and </a> is treated as one line
            # and is added to the previous line
            if ('href' in line or isInsideHref):
                linesFormatted[-1] = linesFormatted[-1].strip() + ' ' + line.strip()
                isInsideHref = True

                # End of href reached
                if ('</a>' in line):
                    # Add an extra line break after </a>
                    linesFormatted[-1] = linesFormatted[-1] + '\n'
                    isInsideHref = False
                continue

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
                strong = True
                continue

            if (line.startswith(r'<h2 class="box_title">')):
                boxInNextLine = True
                continue

            linesFormatted.append(lineFormatted)
            # targetFile.write(lineFormatted)

        sourceFile.close()

        index = index =+ 1

    # Join all lines into one string
    content = ''.join(linesFormatted)

    # Do final replacements of weird stuff
    content = replaceStuffInOutputFile(content)

    # Write final content to file
    targetFile.write(content)
    targetFile.close()

if __name__ == '__main__':
    pathWiki = r'output\\wiki.wiki'

    parseHTMLFiles()