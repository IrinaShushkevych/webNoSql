from mongoengine import Document
from mongoengine.fields import StringField, ListField, ReferenceField, DateField

class Authors(Document):
    fullname = StringField(min_length=3, max_length=150)
    born_date = DateField(required=True)
    born_location = StringField(max_length=250)
    description = StringField()



class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField('Authors', reverse_delete_rule=2)
    quote = StringField()
