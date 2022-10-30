import string
import requests
from bs4 import BeautifulSoup
from .html_parser import HtmlParser, Context


# parser for https://www.rainews24.it/...
class RaiHtmlParser(HtmlParser):

    def perform_request(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = fix_title_text(soup.title.text)
        content = fix_content_text(soup.find_all(attrs={"id": "content-to-read"})[0].text)
        return Context(title, content)


def fix_title_text(title):
    return str(title)


def fix_content_text(content):

    content = content.translate({ord(c): ' ' for c in string.whitespace})
    content = content.translate({ord(c): '' for c in '\u00a0'})
    content = content.strip()

    return content
