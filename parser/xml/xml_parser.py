from abc import ABC, abstractmethod


class XmlParser(ABC):

    @classmethod
    @abstractmethod
    def parse(cls):
        pass


class Channel:
    items = []

    def __init__(self, title, description, link, language="it"):
        self.title = title
        self.description = description
        self.link = link
        self.language = language

    def add_item(self, item):
        if _is_contained(self, item.title):
            return False
        self.items.append(item)
        return True

    def __str__(self):
        items = []
        for i in self.items:
            items.append(str(i))
        return "[title=%s, description=%s, link=%s, language=%s, items=[%s]]" \
               % (self.title,
                  self.description,
                  self.link,
                  self.language,
                  items)


class Item:
    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link

    def __str__(self):
        return "[title=%s, description=%s, link=%s]" \
               % (self.title,
                  self.description,
                  self.link)


def _is_contained(channel, title):
    for i in channel.items:
        if i.title == title:
            return True
    return False
