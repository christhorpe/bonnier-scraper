#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


import views
import scrapers
import loaders
import api
import lifters


def main():
	urlmap = [
		('/', views.DefaultHandler),

		('/scrape/feeds', scrapers.FeedQueueHandler),
		('/scrape/feed', scrapers.FeedHandler),
		('/scrape/images', scrapers.ImageDetailsQueue),
		('/scrape/imagedetails', scrapers.ImageDetailsHandler),
		('/scrape/imagecache', scrapers.ImageCacheHandler),
		('/scrape/text', scrapers.TextRetrievalHandler),
		('/scrape/terms', scrapers.TermRetrievalHandler),

		('/scrape/sectionpages', scrapers.SectionPageLinksQueue),
		('/scrape/sectionpage', scrapers.SectionPageLinksHandler),

		('/load/feeds', loaders.FeedsHandler),
		('/load/pages', loaders.SectionsHandler),

		('/api/item', api.ItemHandler),
		('/api/imageitems', api.ItemImageList),
		
		('/lift/sectionpages', lifters.SectionPageListLiftQueue),
		('/lift/sectionpage', lifters.SectionPageListLifter),
		

	]
	application = webapp.WSGIApplication(urlmap, debug=True)
	util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
