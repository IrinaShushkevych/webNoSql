from mongo.models import Authors, Quotes
from mongo.models_message import User, SendsMessages
from mongo.mongo_connect import m_connect
from mongo.seeds import seeds
from mongo.selects import fetch_authors, fetch_quotes