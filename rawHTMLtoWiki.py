from bs4 import BeautifulSoup as bs
from pathlib import Path
import os, glob

def getTitleFromFileName(fileName):
    return fileName.removesuffix('.html')

def buildURL(title):
    return r'https://dev.arma3.com/post/' + title.lower()

def buildURLWiki(url, title):
    return r'{{Link|' + url + '|' + title + r'}}'

def parseHTMLFiles():
    pathWiki = r'output\\wiki.txt'

    targetFile = open(pathWiki, 'w+', encoding='utf-8')

    # Get all source files
    path = os.path.join('output', '*.html')

    # Sort the files because first two spotreps have diff. name
    files = sorted(glob.glob(path), key=os.path.getctime)

    # Loop over all source files

    index = 0

    for sourceFile in files:
        sourceFile = open(sourceFile, 'r', encoding='utf-8')

        title = getTitleFromFileName(os.path.basename(sourceFile.name))
        sectionTitle = f'== {title} =='
        url = buildURL(title)
        wikiLink = buildURLWiki(url, title)

        # Add beginning of each SPOTREP
        if index == 0:
            targetFile.writelines([sectionTitle, '\n\n', wikiLink, '\n\n'])
        else:
            targetFile.writelines(['\n\n', sectionTitle, '\n\n', wikiLink, '\n\n'])

        soup = bs(sourceFile, 'html.parser')
        paragraph = soup.p.get_text('\n\n', True)

        targetFile.write(paragraph)

        sourceFile.close()

        index = index =+ 1

    targetFile.close()

if __name__ == '__main__':
    parseHTMLFiles()