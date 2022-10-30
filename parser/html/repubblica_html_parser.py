import string
import requests
from bs4 import BeautifulSoup
from .html_parser import HtmlParser, Context


# parser for https://bari.repubblica.it/...
class RepubblicaHtmlParser(HtmlParser):

    def perform_request(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = fix_title_text(soup.title.text)
        article_body_array = soup.find_all(attrs={"id": "article-body"})
        content = ""

        if article_body_array:
            content = fix_content_text(article_body_array[0].text)

        return Context(title, content)


def fix_title_text(title):
    return title


def fix_content_text(content):

    content = content.translate({ord(c): ' ' for c in string.whitespace})
    content = content.translate({ord(c): '' for c in '\u00a0'})
    content = content.strip()

    return content
