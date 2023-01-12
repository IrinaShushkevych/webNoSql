# docker run --name redis-cache -d -p 6379:6379 redis
import redis
from redis_lru import RedisLRU
import json
from bson import json_util
import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

host = conf.get('redis', 'host')
port = conf.get('redis', 'port')
password = conf.get('redis', 'password') if conf.get('redis', 'password') else None
db = conf.get('redis', 'db')

r_connect = redis.StrictRedis(host=host, port=port, password=password, db=db)
cache = RedisLRU(r_connect)

def set(key, value):
    r_connect.set(key, json_util.dumps(value), ex=120)

def get(key):
    result = r_connect.get(key)
    return json.loads(result) if result else None