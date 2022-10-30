import string

from data import get_mongo, find_one, insert_one, Data
from parser.xml import AnsaXmlParser
from parser.html import AnsaHtmlParser


def perform_ansa():
    ansa_xml_parser = AnsaXmlParser("https://www.ansa.it/puglia/notizie/puglia_rss.xml")
    ansa_channel = ansa_xml_parser.parse()

    for item in ansa_channel.items:
        ansa_html_parser = AnsaHtmlParser(item.link)
        context = ansa_html_parser.perform_request()
        _add_to_database(item.title, context.content, item.pub_date)


def _add_to_database(title: string, raw_text: string, created_at: string):
    database = get_mongo().ansa
    result = find_one(database, {"title": title})

    if result is None:
        data = Data(author_name="ansa.it",
                    author_username="ansa.it",
                    title=title,
                    raw_text=raw_text,
                    created_at=created_at)
        insert_one(database, data)
        print("saving of: " + str(data))
