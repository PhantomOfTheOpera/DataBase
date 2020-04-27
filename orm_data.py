import json
import json_handler as j
import peewee as p

db = p.SqliteDatabase('news.db')


class News(p.Model):
    id = p.AutoField()
    time = p.TextField()
    source = p.TextField()
    title = p.TextField()
    url = p.TextField(unique=True)
    content = p.TextField()

    class Meta:
        database = db


def database_fill(filename):
    str_data = open(filename).read()
    json_data = json.loads(str_data)
    if j.check_response(json_data):
        for entry in json_data['articles']:
            time, source, title, url, content = j.article_categorizer(entry)

            article = News(time=time, source=source, title=title, url=url, content=content)
            article.save()


db.connect()
db.create_tables([News])
database_fill('gb.json')