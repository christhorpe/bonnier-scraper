from google.appengine.ext import db


class Section(db.Model):
	section_url = db.StringProperty()
	label = db.StringProperty()
	last_scraped = db.DateTimeProperty()
	last_hash = db.StringProperty()


class SectionPageList(db.Model):
	section = db.ReferenceProperty(Section)
	section_datekey = db.StringProperty
	section_scraped = db.DateTimeProperty(auto_now_add=True)
	pagelist = db.StringListProperty()
	processed = db.BooleanProperty(default=False)


class Feed(db.Model):
	feed_url = db.StringProperty()
	label = db.StringProperty()
	last_scraped = db.DateTimeProperty()
	last_hash = db.StringProperty()


class Item(db.Model):
	item_url = db.StringProperty()
	title = db.StringProperty()
	category = db.StringProperty()
	sectionlist = db.StringListProperty()
	byline = db.StringProperty()
	description = db.TextProperty()
	pubDate = db.StringProperty()
	pub_date = db.DateTimeProperty()
	last_scraped = db.DateTimeProperty()
	scraped = db.BooleanProperty(default=False)
	img_url = db.StringProperty()
	img = db.BlobProperty()
	has_img = db.BooleanProperty(default=False)
	img_scraped = db.BooleanProperty(default=False)
	standfirst = db.TextProperty()




class Facet(db.Model):
	name = db.StringProperty()
	itemlist = db.StringListProperty()


class Collection(db.Model):
	page = db.StringProperty()
	collection_datetime = db.DateTimeProperty()
	collection = db.StringListProperty()


class DaySectionPage(db.Model):
	page = db.StringProperty()
	section = db.StringProperty()
	day = db.StringProperty()
	count = db.IntegerProperty(default=0)
