from abc import ABC, abstractmethod


class HtmlParser(ABC):
    def __init__(self, url):
        self.url = url

    @classmethod
    @abstractmethod
    def perform_request(cls):
        pass

    def __str__(self):
        return "[URL=%s]" % self.url


class Context:

    def __init__(self, title, content, language="it"):
        self.title = title
        self.content = content
        self.language = language

    def __str__(self):
        return "[title=%s, content=%s, language=%s]" \
               % (self.title,
                  self.content,
                  self.language)
