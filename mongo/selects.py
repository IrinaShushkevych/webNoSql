from mongo import Authors, Quotes
from redis_cache import cache

# @cache
def fetch_authors(name):
    print('FETCH AUTHOR')
    author = Authors.objects(fullname__iregex = name)
    result = []
    for el in author:
        result.append(el.to_mongo().to_dict())
    return result

# @cache
def fetch_quotes(tags):
    print('FETCH QUOTE')
    quote = Quotes.objects(tags__iregex = tags)
    result = []
    for el in quote:
        author = el.author.fullname
        res = el.to_mongo().to_dict()
        res['author'] = author
        result.append(res)
    return result

