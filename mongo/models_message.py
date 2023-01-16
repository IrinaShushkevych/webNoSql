from mongoengine import Document
from mongoengine.fields import StringField, ListField, ReferenceField, EmailField, BooleanField

class User(Document):
    firstname = StringField(min_length=3, max_length=50, required=True)
    lastname = StringField(max_length=50)
    email = EmailField()
    phone = StringField(min_length=10, max_length=30)
    method = StringField(choices=['sms', 'email'])
    message_sends = BooleanField(default=False)
