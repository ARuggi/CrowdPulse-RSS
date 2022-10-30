import string

from data import get_mongo, find_one, insert_one, Data
from parser.xml import TheSunXmlParser


def perform_the_sun():
    the_sun_xml_parser = TheSunXmlParser("https://www.thesundaily.my/rss/home")
    the_sun_channel = the_sun_xml_parser.parse()

    for item in the_sun_channel.items:
        # the_sun_html_parser = TheSunHtmlParser(item.link)
        # context = the_sun_html_parser.perform_request()
        _add_to_database(item.title, item.description, item.pub_date)


def _add_to_database(title: string, raw_text: string, created_at: string):
    database = get_mongo().the_sun
    result = find_one(database, {"title": title})

    if result is None:
        data = Data(author_name="thesundaily.my",
                    author_username="thesundaily.my",
                    title=title,
                    lang="en",
                    raw_text=raw_text,
                    created_at=created_at)
        insert_one(database, data)
        print("saving of: " + str(data))
