import string

from data import get_mongo, find_one, insert_one, Data
from parser.xml import RaiXmlParser
from parser.html import RaiHtmlParser


def perform_rai():
    rai_xml_parser = RaiXmlParser("https://www.rai.it/dl/portale/html/PublishingBlock-15c2c340-e282-473d-b944"
                                  "-661e818d667b-rss.xml")
    rai_channel = rai_xml_parser.parse()

    for item in rai_channel.items:
        rai_html_parser = RaiHtmlParser(item.link)
        context = rai_html_parser.perform_request()
        _add_to_database(item.title, context.content, item.pub_date)


def _add_to_database(title: string, raw_text: string, created_at: string):
    database = get_mongo().rai
    result = find_one(database, {"title": title})

    if result is None:
        data = Data(author_name="rainews.it",
                    author_username="rainews.it",
                    title=title,
                    raw_text=raw_text,
                    created_at=created_at)
        insert_one(database, data)
        print("saving of: " + str(data))
