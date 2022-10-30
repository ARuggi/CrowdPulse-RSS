import string
import requests
from bs4 import BeautifulSoup
from .html_parser import HtmlParser, Context


# parser for https://www.ansa.it/puglia/notizie/...
class AnsaHtmlParser(HtmlParser):

    def perform_request(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = fix_title_text(soup.title.text)
        content = fix_content_text(soup.find_all(attrs={"itemprop": "articleBody"})[0].text)
        return Context(title, content)


def fix_title_text(title):
    title = str(title)
    if title.endswith(" - Puglia - ANSA.it"):
        title = title[0:title.index(" - Puglia - ANSA.it")]
    return title


def fix_content_text(content):

    content = content.translate({ord(c): ' ' for c in string.whitespace})
    content = content.translate({ord(c): '' for c in '\u00a0'})
    content = content.strip()

    if content.startswith("(ANSA) - "):
        content = content[len("(ANSA) - "):len(content)]
    if content.endswith(" (ANSA)."):
        content = content[0:content.index(" (ANSA).")]

    # removing of: "BARI 05 SET -" starting line if present
    i = content.find(" - ")
    if i > 0:
        content = content[i + len(" - "):len(content)]

    return content
