import string

from data import get_mongo, find_one, insert_one, Data
from parser.xml import Sole24XmlParser


def perform_sole24():
    sole24_xml_parser = Sole24XmlParser("https://www.ilsole24ore.com/rss/italia--attualita.xml")
    sole24_channel = sole24_xml_parser.parse()

    for item in sole24_channel.items:
        # sole24_html_parser = TheSunHtmlParser(item.link)
        # context = sole24_html_parser.perform_request()
        _add_to_database(item.title, item.description, item.pub_date)


def _add_to_database(title: string, raw_text: string, created_at: string):
    database = get_mongo().sole24
    result = find_one(database, {"title": title})

    if result is None:
        data = Data(author_name="ilsole24ore.com",
                    author_username="ilsole24ore.com",
                    title=title,
                    raw_text=raw_text,
                    created_at=created_at)
        insert_one(database, data)
        print("saving of: " + str(data))
