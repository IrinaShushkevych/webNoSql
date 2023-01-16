# docker run --name redis-cache -d -p 6379:6379 redis
import redis
from redis_lru import RedisLRU
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

def r_cache(max_count=3):
    def redis_cache(func):
        def wrapper(*args, **kwargs):
            list_name = 'mdb_list'
            param = f'{func.__name__}:'
            if args:
                param +=' '.join(args)
            if kwargs:
                param +=' '.join([value for key, value in kwargs.items()])
            list_len = r_connect.llen(list_name)
            r_list = r_connect.lrange(list_name, 0, -1)
            try:
                index_el = r_list.index(param.encode())
            except ValueError:
                index_el = None
            if index_el:
                if index_el > 0:
                    el = r_connect.lrem(list_name, 1, param.encode())
                    r_connect.lpush(list_name, param)
                result = json_util.loads(r_connect.get(param))
            else:
                if list_len == max_count:
                    el = r_connect.rpop(list_name)
                    r_connect.delete(el)
                r_connect.lpush(list_name, param)
                result = func(*args, *kwargs)
                r_connect.set(param, json_util.dumps(result))
            return result
        return wrapper
    return redis_cache