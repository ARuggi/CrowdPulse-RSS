import string

from data import get_mongo, find_one, insert_one, Data
from parser.xml import RepubblicaXmlParser
from parser.html import RepubblicaHtmlParser


def perform_repubblica():
    _perform_homepage()
    _perform_cronaca()


def _perform_homepage():
    _perform("https://bari.repubblica.it/rss/rss2.0.xml")


def _perform_cronaca():
    _perform("https://bari.repubblica.it/rss/cronaca/rss2.0.xml")


def _perform(url: string):
    repubblica_xml_parser = RepubblicaXmlParser(url)
    repubblica_channel = repubblica_xml_parser.parse()

    for item in repubblica_channel.items:
        repubblica_html_parser = RepubblicaHtmlParser(item.link)
        context = repubblica_html_parser.perform_request()
        _add_to_database(item.title, context.content, item.pub_date)


def _add_to_database(title: string, raw_text: string, created_at: string):

    #print("[%s] - %s >>> %s", created_at, title, raw_text)

    database = get_mongo().repubblica
    result = find_one(database, {"title": title})

    if result is None:
        data = Data(author_name="repubblica.it",
                    author_username="repubblica.it",
                    title=title,
                    raw_text=raw_text,
                    created_at=created_at)
        insert_one(database, data)
        print("saving of: " + str(data))
