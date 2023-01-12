from mongoengine import connect
import configparser

conf = configparser.ConfigParser()
conf.read('settings.ini')

m_user = conf.get('mongo', 'user')
m_pass = conf.get('mongo', 'pass')
m_db = conf.get('mongo', 'db_name')
m_domain = conf.get('mongo', 'domain')

url = f'mongodb+srv://{m_user}:{m_pass}@{m_domain}/{m_db}?retryWrites=true&w=majority'
m_connect = None

try:
    m_connect = connect(host=url, ssl=True)
except:
    print('Connection to database failed')
    quit()
