
import mongoengine
from mongoengine import fields, Document, ImproperlyConfigured
from creators.models import Creator

def make_ngrams(word, min_size=2):
    length = len(word)
    size_range = range(min_size, max(length, min_size) + 1)
    return list(set(
        word[i:i + size]
        for size in size_range
        for i in range(0, max(0, length - size) + 1)
    ))

class Book(Document):
	title = fields.StringField(required=True)
	isbns = fields.ListField(fields.StringField(unique=True), required=True)
	authors = fields.ListField(fields.StringField(), required=True)
	covers = fields.ListField(fields.StringField(), required=True)
	publisher = fields.ReferenceField(Creator, reverse_delete_rule=mongoengine.CASCADE,
		required=False, read_only=True)
	active = fields.BooleanField(default=True)
	ngrams = fields.StringField()

	meta = {'indexes': [
        {
			'fields': ['$ngrams'],
        	'default_language': 'english',
        }
    ]}

	def save(self, *args, **kwargs):
		ngrams = []
		for word in self.title.split():
			ngrams.extend(make_ngrams(word))
		self.ngrams = ' '.join(ngrams)
		return super(Book, self).save(*args, **kwargs)

class Content(Document):
	title = fields.StringField(required=True)
	description  =fields.StringField(required=True)
	images = fields.ListField(fields.StringField(required=True), required=True)
	file  = fields.StringField(required=True)
	creator = fields.ReferenceField(Creator, read_only=True)
	book = fields.ReferenceField(Book, required=True, reverse_delete_rule=mongoengine.CASCADE)
	active = fields.BooleanField(default=True)
	size = fields.IntField(default=4000)
	animated = fields.BooleanField(default=False)