from google.appengine.ext import webapp

import models

class FeedsHandler(webapp.RequestHandler):
	def get(self):
		feeds = [
			{"url":"http://www.dn.se/m/rss/senaste-nytt", "label":"SENASTE NYTT"},
			{"url":"http://www.dn.se/sthlm/m/rss/senaste-nytt", "label":"STOCKHOLMSNYHETERNA"},
			{"url":"http://www.dn.se/ekonomi/m/rss", "label":"EKONOMINYHETERNA"},
			{"url":"http://www.dn.se/sport/m/rss/senaste-nytt", "label":"SPORTNYHETERNA"},
			{"url":"http://www.dn.se/kultur-noje/m/rss/senaste-nytt", "label":"FRAN KULTUR"},
			{"url":"http://www.dn.se/kultur-noje/m/rss/kronikor", "label":"KRONIKORNA"},
			{"url":"http://www.dn.se/kultur-noje/film-tv/m/rss/senaste-nytt", "label":"FRAN FILM/TV"},
			{"url":"http://www.dn.se/dnbok/m/rss/bokrecensioner", "label":"BOKRECENSIONERNA"},
			{"url":"http://www.dn.se/kultur-noje/musik/m/rss/senaste-nytt", "label":"FRAN MUSIK"},
			{"url":"http://www.dn.se/opinion/m/rss/debatt", "label":"DEBATTARTIKLARNA"},
			{"url":"http://www.dn.se/opinion/m/rss/ledare", "label":"HUVUDLEDARNA"},
			{"url":"http://www.dn.se/mat-dryck/m/rss/recept", "label":"RECEPTEN"},
		]
		for feed in feeds:
			models.Feed.get_or_insert(feed['url'], feed_url=feed['url'], label=feed['label'])
			self.response.out.write(feed['url'])
			self.response.out.write(" : ")
			self.response.out.write(feed['label'])
			self.response.out.write("<br />")


class SectionsHandler(webapp.RequestHandler):
	def get(self):
		sections = [
			{"url":"http://www.dn.se/", "label":"Forstasidan"},
			{"url":"http://www.dn.se/nyheter/sverige/", "label":"Sverige"},
			{"url":"http://www.dn.se/nyheter/valet2010/", "label":"Valet2010"},
			{"url":"http://www.dn.se/nyheter/varlden/", "label":"Varlden"},
			{"url":"http://www.dn.se/nyheter/vetenskap/", "label":"Vetenskap"},
			{"url":"http://www.dn.se/sthlm/", "label":"STHLM"},
			{"url":"http://www.dn.se/sthlm/sthlmfordjupning/", "label":"STHLM Fordjupning"},
			{"url":"http://www.dn.se/ekonomi/", "label":"Ekonomi"},
			{"url":"http://www.dn.se/ekonomi/din-ekonomi/", "label":"Din Ekonomi"},
			{"url":"http://www.dn.se/sport/", "label":"Sport"},
			{"url":"http://www.dn.se/sport/fotboll/", "label":"Fotboll"},
			{"url":"http://www.dn.se/sport/ishockey/", "label":"Ishockey"},
			{"url":"http://www.dn.se/sport/os-vancouver/", "label":"OS2010"},
			{"url":"http://www.dn.se/kultur-noje/", "label":"Kulture"},
			{"url":"http://www.dn.se/dnbok/", "label":"DN Bok"},
			{"url":"http://www.dn.se/kultur-noje/debatt-essa/", "label":"Kulturdebatt"},
			{"url":"http://www.dn.se/kultur-noje/essa/", "label":"Essa"},
			{"url":"http://www.dn.se/kultur-noje/film-tv/", "label":"Film TV"},
			{"url":"http://www.dn.se/kultur-noje/konst-form/", "label":"Konst Form"},
			{"url":"http://www.dn.se/kultur-noje/musik/", "label":"Music"},
			{"url":"http://www.dn.se/kultur-noje/scen/", "label":"Scen"},
			{"url":"http://www.dn.se/spel/", "label":"Spel"},
			{"url":"http://www.dn.se/opinion/", "label":"Opinion"},
			{"url":"http://www.dn.se/opinion/debatt/", "label":"Debatt"},
			{"url":"http://www.dn.se/opinion/huvudledare/", "label":"Huvudledare"},
			{"url":"http://www.dn.se/opinion/signerat/", "label":"Signerat"},
			{"url":"http://www.dn.se/opinion/kolumner/", "label":"Kolumner"},
			{"url":"http://www.dn.se/resor/", "label":"Resor"},
			{"url":"http://www.dn.se/mat-dryck/", "label":"Mat Dryck"},
			{"url":"http://www.dn.se/mat-dryck/reportage/", "label":"Mat Dryck Reportage"},
			{"url":"http://www.dn.se/mat-dryck/dryck/", "label":"Mat Dryck Dryck"},
			{"url":"http://www.dn.se/livsstil/", "label":"Livsstil"},
			{"url":"http://www.dn.se/livsstil/intervjuer/", "label":"Livsstil Intervjuer"},
			{"url":"http://www.dn.se/livsstil/livsstilsreportage/", "label":"Livsstil Reportage"},
			{"url":"http://www.dn.se/livsstil/halsa/", "label":"Livsstil Halsa"},
			{"url":"http://www.dn.se/livsstil/relationer/", "label":"Livsstil Relationer"},
			{"url":"http://www.dn.se/livsstil/trend/", "label":"Livsstil Trend"},
			{"url":"http://www.dn.se/insidan/", "label":"Insidan"},
			{"url":"http://www.dn.se/livsstil/livsstilsbloggar/", "label":"Livsstil Bloggar"},
		]
		for section in sections:
			models.Section.get_or_insert(section['url'], section_url=section['url'], label=section['label'])
			self.response.out.write(section['url'])
			self.response.out.write(" : ")
			self.response.out.write(section['label'])
			self.response.out.write("<br />")
