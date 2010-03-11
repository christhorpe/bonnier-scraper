from google.appengine.ext import webapp

import models

class DefaultHandler(webapp.RequestHandler):
	def get(self):
		items = models.Item.all()
		for item in items:
			self.response.out.write(item.title)
			self.response.out.write("<br />")

