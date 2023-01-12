import os
import json
from datetime import datetime
from mongo import  Authors, Quotes

def add_author():
    Authors.drop_collection()

    authors = []
    with open(os.path.join('data', 'authors.json'), 'r') as f:
        res = f.read()
        authors = json.loads(res)

    for el in authors:
        author = Authors(
            fullname = el['fullname'],
            born_date = datetime.strptime(el['born_date'], '%B %d, %Y'),
            born_location = el['born_location'],
            description = el['description']
        )
        author.save()

def add_quotes():
    Quotes.drop_collection()

    quotes = []
    with open(os.path.join('data', 'qoutes.json'), 'r') as f:
        res = f.read()
        quotes = json.loads(res)

    for el in quotes:
        author = Authors.objects.get(fullname=el['author'])
        if not author:
            print('---------------------------------------------------------')
            print('Author', el['author'], 'not found')
            print(" Quote didn't add: ")
            print(el)
            print('---------------------------------------------------------')
        else:
            quote = Quotes(
                tags = el['tags'],
                author = author,
                quote = el['quote']
            )
            quote.save()

def seeds():
    add_author()
    add_quotes()