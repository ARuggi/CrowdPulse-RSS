import string

from data import get_mongo, find_one, insert_one, Data
from parser.xml import CorriereXmlParser
from parser.html import CorriereHtmlParser


def perform_corriere():
    corriere_xml_parser = CorriereXmlParser("http://xml2.corriereobjects.it/rss/cronache.xml")
    corriere_channel = corriere_xml_parser.parse()

    for item in corriere_channel.items:
        corriere_html_parser = CorriereHtmlParser(item.link)
        context = corriere_html_parser.perform_request()
        _add_to_database(item.title, context.content, item.pub_date)


def _add_to_database(title: string, raw_text: string, created_at: string):
    database = get_mongo().corriere
    result = find_one(database, {"title": title})

    if result is None:
        data = Data(author_name="corriere.it",
                    author_username="corriere.it",
                    title=title,
                    raw_text=raw_text,
                    created_at=created_at)
        insert_one(database, data)
        print("saving of: " + str(data))
