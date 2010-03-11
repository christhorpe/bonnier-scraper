from google.appengine.ext import webapp
from google.appengine.api.labs import taskqueue


import models


class SectionPageListLiftQueue(webapp.RequestHandler):
	def get(self):
		sectionpagelists = models.SectionPageList.all()
		for sectionpagelist in sectionpagelists:
			taskqueue.add(url='/lift/sectionpage', params={'key': sectionpagelist.key().name()}, method='GET')	
			self.response.out.write(sectionpagelist.key().name())
			self.response.out.write("<br />")		


class SectionPageListLifter(webapp.RequestHandler):
	def get(self):
		key = self.request.get("key")
		day = key[0:8]
		section = key[10:len(key)].replace("http://www.dn.se/", "")
		if len(section) == 0:
			section = "home"
		if section[len(section)-1] == "/":
			section = section[0:len(section)-1]
		self.response.out.write(day)
		self.response.out.write("<br />")		
		self.response.out.write(section)
		self.response.out.write("<br />")		
		sectionpage = models.SectionPageList.get_by_key_name(key)
		if sectionpage.processed != True:
			for page in sectionpage.pagelist:
				daykey = day + section + page
				dayrecord = models.DaySectionPage.get_or_insert(daykey, day=day, page=page, section=section)
				dayrecord.count +=1
				dayrecord.put()
				self.response.out.write(daykey)
				self.response.out.write("<br />")
			sectionpage.processed = True
			sectionpage.put()