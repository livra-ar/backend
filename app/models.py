
import mongoengine
from mongoengine import fields, Document, ImproperlyConfigured
from creators.models import Creator

class Book(Document):
	title = fields.StringField(required=True)
	isbns = fields.ListField(fields.StringField(), required=True)
	authors = fields.ListField(fields.StringField(), required=True)
	covers = fields.ListField(fields.StringField(), required=True)
	publisher = fields.ReferenceField(Creator, reverse_delete_rule=mongoengine.CASCADE,
		required=False, read_only=True)
	content =  fields.ListField(fields.ReferenceField('Content'), required=False)

class Content(Document):
	title = fields.StringField(required=True)
	description  =fields.StringField(required=True)
	images = fields.ListField(fields.StringField(required=True))
	file  = fields.StringField(required=True)
	creator = fields.ReferenceField(Creator, read_only=True)
	book = fields.ReferenceField('Book',required=True, reverse_delete_rule=mongoengine.CASCADE)
	active = fields.BooleanField(default=False)
