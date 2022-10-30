import pymongo


class Data:

    def __init__(self, _id=-1, author_name="", author_username="", title="", lang="it", raw_text="", created_at=""):
        self._id = _id
        self.author_name = author_name
        self.author_username = author_username
        self.lang = lang
        self.title = title
        self.raw_text = raw_text
        self.created_at = created_at

    def __str__(self):
        if self._id < 0:
            return "[author_name=%s, author_username=%s, title=%s, lang=%s, raw_text=%s, created_at=%s" \
                   % (self.author_name,
                      self.author_username,
                      self.title,
                      self.lang,
                      self.raw_text,
                      self.created_at)
        else:
            return "[ID=%s, author_name=%s, author_username=%s, title=%s, lang=%s, raw_text=%s, created_at=%s" \
                   % (self._id,
                      self.author_name,
                      self.author_username,
                      self.title,
                      self.lang,
                      self.raw_text,
                      self.created_at)


def get_mongo():
    return pymongo.MongoClient("mongodb://localhost:27017/")["test-database"]


# noinspection PyProtectedMember
def insert_one(database: pymongo.MongoClient, data: Data):

    if (data.raw_text is None) or (not data.raw_text.strip()):
        raise Exception("The raw text cannot be empty")

    raw_data = {
        "author_name": data.author_name,
        "author_username": data.author_username,
        "title": data.title,
        "lang": data.lang,
        "raw_text": data.raw_text,
        "created_at": data.created_at
    }

    database.insert_one(raw_data)


# noinspection PyProtectedMember
def find_one(database: pymongo.MongoClient, expression):

    result = database.find_one(expression)

    if result is not None:
        return Data(
            author_name=result["author_name"],
            author_username=result["author_username"],
            title=result["title"],
            lang=result["lang"],
            raw_text=result["raw_text"],
            created_at=result["created_at"])

    return None

