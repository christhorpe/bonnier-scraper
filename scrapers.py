import hashlib
import datetime

from google.appengine.ext import webapp
from google.appengine.api.labs import taskqueue
from google.appengine.api import urlfetch
from google.appengine.api import images

import helpers
import models

class FeedQueueHandler(webapp.RequestHandler):
	def get(self):
		feeds = models.Feed.all()
		for feed in feeds:
			taskqueue.add(url='/scrape/feed', params={'name': feed.label, "url":feed.feed_url}, method='GET')
			self.response.out.write(feed.label)
			self.response.out.write("<br />")


class FeedHandler(webapp.RequestHandler):
	def get(self):
		url = self.request.get("url")
		query = "select title, link, description, category.content, creator, pubDate, link from rss where url='"+ url +"'"
		result = helpers.do_yql(query)
		feed = models.Feed.get_by_key_name(url)
		resulthash = hashlib.md5(str(result)).hexdigest()
		feed.last_hash = resulthash
		feed.last_scraped = datetime.datetime.today()
		self.response.out.write(resulthash)
		self.response.out.write("<br />")
		self.response.out.write("<br />")
		try:
			for element in result['query']['results']['item']:
				models.Item.get_or_insert(element['link'], item_url=element['link'], title=element['title'], category=element['category'], description=element['description'], byline=element['creator'], pubDate=element['pubDate'])
				self.response.out.write(element['category'])
				self.response.out.write("<br />")
				self.response.out.write(element['description'])
				self.response.out.write("<br />")
				self.response.out.write(element['title'])
				self.response.out.write("<br />")
				self.response.out.write(element['pubDate'])
				self.response.out.write("<br />")
				self.response.out.write(element['creator'])
				self.response.out.write("<br />")
				self.response.out.write(element['link'])
				self.response.out.write("<br />")
				self.response.out.write("<br />")
		except:
			self.response.out.write("fail")
		feed.put()


class SectionPageLinksQueue(webapp.RequestHandler):
	def get(self):
		sections = models.Section.all()
		for section in sections:
			taskqueue.add(url='/scrape/sectionpage', params={"url":section.section_url}, method='GET')
			self.response.out.write(section.label)
			self.response.out.write("<br />")


class SectionPageLinksHandler(webapp.RequestHandler):
	def get(self):
		url = self.request.get("url")
		section = models.Section.get_by_key_name(url)
		query = "select * from html where url = '"+ url +"' and xpath='//div[@id=\"main\"]//a'"
		result = helpers.do_yql(query)
#		self.response.out.write(result)
		resulthash = hashlib.md5(str(result)).hexdigest()
		section.last_hash = resulthash
		section.last_scraped = datetime.datetime.today()
		linklist = []
		for link in result['query']['results']['a']:
			if not "http://www.newsmill.se" in link['href']:
				if not "http://www.pastan.nu" in link['href']:
					if not "http://www.nyteknik.se" in link['href']:
						if not "http://www.alltommotor.se" in link['href']:
							if not "http://www.motimate.se" in link['href']:
								if not "http://altfarm.mediaplex.com" in link['href']:
									if not "http://affiliate.se.espotting.com" in link['href']:
										if not "mailto:" in link['href']:
											if "http://www.dn.se" in link['href']:
												linkurl = link['href']
											else:
												linkurl = "http://www.dn.se" + link['href']
											linkurl = linkurl.replace("#article-readers", "")
											if linkurl not in linklist:
												linklist.append(linkurl)
		datekey = str(datetime.datetime.today()).replace("-", "").replace(" ", "")[0:10]
		sectionkey = datekey + url
		sectionpagelist = models.SectionPageList.get_or_insert(sectionkey, section=section, section_datekey=datekey, pagelist=linklist)
		self.response.out.write(sectionkey + "<br />")
		self.response.out.write(str(datetime.datetime.today()) + "<br />")
		self.response.out.write(str(len(linklist)) + "<br />")
		self.response.out.write(str(linklist) + "<br />")
		section.put()



class ImageDetailsHandler(webapp.RequestHandler):
	def get(self):
		url = self.request.get("url")
		item = models.Item.get_by_key_name(url)
		query = "select src, height, width from html where url='"+ url +"' and xpath='//div[@id=\"main\"]//img' and height > 200 and width > 200"
		result = helpers.do_yql(query)
		self.response.out.write(url)
		self.response.out.write("<br />")
		imgurl = False
		try:
			element = result['query']['results']['img'][0]
			if "www.dn.se" in element['src']:
				imgurl = element['src']
			else:
				imgurl = "http://www.dn.se%s" % (element['src'])
			self.response.out.write("<img src=\"%s\"/>" % imgurl)
			if imgurl:
				item.img_url = imgurl
			else:
				item.img_url = False
			item.put()
			self.response.out.write("<br />")
			self.response.out.write(imgurl)
		except:
			self.response.out.write(result)
		self.response.out.write("<br />")
		if item:
			self.response.out.write("is an item")
			taskqueue.add(url='/scrape/imagecache', params={"url":item.item_url, "imgurl":imgurl}, method='GET')
		else:
			self.response.out.write("scrape item")
		self.response.out.write("<br />")




class ImageDetailsQueue(webapp.RequestHandler):
	def get(self):
		items = models.Item.all().filter('img_url =', None)
		for item in items:
			taskqueue.add(url='/scrape/imagedetails', params={"url":item.item_url}, method='GET')
			self.response.out.write(item.item_url + "<br />")
		

class ImageCacheHandler(webapp.RequestHandler):
	def get(self):
		url = self.request.get("url")
		imgurl = self.request.get("imgurl")
		if imgurl != "False":
			item = models.Item.get_by_key_name(url)
			request = urlfetch.fetch(url=imgurl, method=urlfetch.GET)
			image = helpers.crop_image(request.content, 200)
			if image:
				if item:
					item.img = image
					item.has_img = True
					item.img_scraped = True
					item.put()
			self.response.headers['Content-Type'] = 'image/jpeg'
			self.response.out.write(image)
			


class TextRetrievalHandler(webapp.RequestHandler):
	def get(self):
		url = self.request.get("url")
		request = urlfetch.fetch(url=url, method=urlfetch.GET)
		self.response.out.write(request.content.replace("a href=\"http://www.dn.se/\"", "a href=\"http://localhost:8116/scrape/text?url=http://www.dn.se/\""))


class TermRetrievalHandler(webapp.RequestHandler):
	def get(self):
		context = """
		"""
		query = "http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction?appid=dzuTJH3V34F6pTHQnDGtWt_adJnFoFh70qERrfH5PyTaWUq8mS9BJAsL7VT9fZI&context=%s" % context
		request = urlfetch.fetch(url=url, method=urlfetch.GET)
		self.response.out.write(request.content)
		