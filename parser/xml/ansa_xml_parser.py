import requests
from bs4 import BeautifulSoup
from .xml_parser import XmlParser, Channel, Item


class AnsaXmlParser(XmlParser):

    def __init__(self, url):
        self.url = url

    # noinspection PyUnresolvedReferences
    def parse(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'xml')
        result = None

        rss = soup.find("rss")
        for channel in rss.find_all("channel"):

            title = channel.title.text
            description = channel.description.text
            link = channel.link.attrs["href"]
            language = channel.language.text
            result = AnsaChannel(title, description, link, language)

            for item in channel.find_all_next("item"):
                title = item.title.text
                description = item.description.text
                link = item.link.text
                pub_date = item.pubDate.text
                result.add_item(AnsaItem(title, description, link, pub_date))

        return result


class AnsaChannel(Channel):
    def __init__(self, title, description, link, language):
        super().__init__(title, description, link, language)


class AnsaItem(Item):
    def __init__(self, title, description, link, pub_date):
        super().__init__(title, description, link)
        self.pub_date = pub_date

    def __str__(self):
        return "[title=%s, description=%s, link=%s, pub_date=%s]" \
               % (self.title,
                  self.description,
                  self.link,
                  self.pub_date)
