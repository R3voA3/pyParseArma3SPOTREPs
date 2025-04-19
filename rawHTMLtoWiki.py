from bs4 import BeautifulSoup as bs

def parseHTMLFile():
    pathRawHTML = r"output\rawHTML.txt"
    pathWiki = r"output\wiki.txt"

    # Format sourceFile
    # sourceFile = open(pathRawHTML,"r", encoding="utf-8")
    # targetFile = open(pathWiki,"w+", encoding="utf-8")

    with open(pathRawHTML, 'r', encoding='utf-8') as file:
        soup = bs(file, 'html.parser')

    test = soup.find_all("li")
    print(test)

if __name__ == '__main__':
    parseHTMLFile()