from google.appengine.ext import webapp

import models

class ItemHandler(webapp.RequestHandler):
	def get(self):
		url = self.request.get("url")
		item = models.Item.get_by_key_name(url)
		self.response.out.write("{\n")
		self.response.out.write("\"title\":\"" + item.title + "\",\n")
		self.response.out.write("\"category\":\"" + item.category + "\",\n")
		if item.byline is not None:
			self.response.out.write("\"byline\":\"" + item.byline + "\",\n")
		self.response.out.write("\"url\":\"" + item.item_url + "\",\n")
		if item.img_url is not None:
			self.response.out.write("\"imgurl\":\"" + item.img_url + "\",\n")
		if item.description is not None:
			self.response.out.write("\"description\":\"" + item.description + "\",\n")
		self.response.out.write("\"pubdate\":\"" + item.pubDate + "\"\n")
		self.response.out.write("}\n")
		


class ItemImageList(webapp.RequestHandler):
	def get(self):
		items = models.Item.all().filter('img_url !=', None)
		self.response.out.write("{")
		self.response.out.write("\"items\":[")
		i=0
		n=0
		for firstrun in items:
			n += 1
		for item in items:
			self.response.out.write("{")
			self.response.out.write("\"url\":\"" + item.item_url + "\",")
			self.response.out.write("\"imgurl\":\"" + item.img_url + "\",")
			self.response.out.write("\"title\":\"" + item.title + "\",")
			self.response.out.write("\"pubdate\":\"" + item.pubDate + "\"")
			if i == (n - 1):
				self.response.out.write("}")
			else:
				self.response.out.write("},")
			i += 1
		self.response.out.write("]")
		self.response.out.write("}")



