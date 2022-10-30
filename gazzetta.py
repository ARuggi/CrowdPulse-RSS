import string

from data import get_mongo, find_one, insert_one, Data
from parser.xml import GazzettaXmlParser
from parser.html import GazzettaHtmlParser


def perform_gazzetta():
    gazzetta_xml_parser = GazzettaXmlParser("https://www.lagazzettadelmezzogiorno.it/rss.jsp?sezione=145")
    gazzetta_channel = gazzetta_xml_parser.parse()

    for item in gazzetta_channel.items:
        gazzetta_html_parser = GazzettaHtmlParser(item.link)
        context = gazzetta_html_parser.perform_request()
        _add_to_database(item.title, context.content, item.pub_date)


def _add_to_database(title: string, raw_text: string, created_at: string):
    database = get_mongo().gazzetta
    result = find_one(database, {"title": title})

    if result is None:
        data = Data(author_name="gazzetta.it",
                    author_username="gazzetta.it",
                    title=title,
                    raw_text=raw_text,
                    created_at=created_at)
        insert_one(database, data)
        print("saving of: " + str(data))
