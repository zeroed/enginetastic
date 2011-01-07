import cgi
import os
import web_spider
import TI3_player_gen_for_Web
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.db import stats

# The webapp module is in the google.appengine.ext package.
# This module is provided in the SDK, as well as in the production runtime environment.

# http://enginetastic.appspot.com

# database Models

class Greeting(db.Model):
	author = db.UserProperty()
	content = db.StringProperty(multiline=True)
	date = db.DateTimeProperty(auto_now_add=True)

class WebUrl(db.Model):
	url = db.StringProperty()
	info = db.TextProperty()
	date = db.DateTimeProperty(auto_now_add=True)
	
class Ti3Match(db.Model):
	number_of_players = db.StringProperty()
	teams_assigned = db.TextProperty()
	info = db.TextProperty()
	date = db.DateTimeProperty(auto_now_add=True)

# This code defines one request handler, MainPage, mapped to the root URL (/).
# When webapp receives an HTTP GET request to the URL /, it instantiates 
# the MainPage class and calls the instance's get method. 
# Inside the method, information about the request is available 
# using self.request. Typically, the method sets properties on self.response 
# to prepare the response, then exits. webapp sends a response based 
# on the final state of the MainPage instance.

class MainPage(webapp.RequestHandler):
	def get(self):
		greetings_query = Greeting.all().order('-date')
		greetings = greetings_query.fetch(5)
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		spider_url = "spiderpage"
		spider_link_text = "Spider Page"
		ti3_url = "ti3page"
		ti3_link_text = "Twilight Imperium player generator"
		#global_stat = stats.GlobalStat.all().get()
		#total_bytes = global_stat.bytes
		#entry_num = global_stat.count
		total_bytes = 0
		entry_num = 0

# template.render(path, template_values) takes a file path 
# to the template file and a dictionary of values, and returns 
# the rendered text. The template uses Django templating syntax 
# to access and iterate over the values, and can refer to properties 
# of those values. In many cases, you can pass datastore model 
# objects directly as values, and access their properties from templates.
		template_values = {
			'url': url,
			'greetings': greetings,
			'url_linktext': url_linktext,
			'spider_link_text': spider_link_text,
			'spider_url': spider_url,
			'ti3_url': ti3_url,
			'ti3_link_text': ti3_link_text,
			'total_bytes': total_bytes,
			'entry_num':  entry_num,
		}
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
	def post(self):
		greeting = Greeting()
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.content = self.request.get('content')
		greeting.put()
		self.redirect('/')

class SpiderPage(webapp.RequestHandler):
	def get(self):
		weburls_query = WebUrl.all().order('-date')
		weburls = weburls_query.fetch(5)
		logged = 'false'
		if users.get_current_user():
			logged = 'true'
		main_link = '/'
		main_link_text = "Home Page"
		#global_stat = stats.GlobalStat.all().get()
		#total_bytes = global_stat.bytes
		#entry_num = global_stat.count
		total_bytes = 0
		entry_num = 0
		template_values = {
			'weburls': weburls,
			'logged': logged,
			'main_link_text': main_link_text,
			'main_link': main_link,
			'total_bytes': total_bytes,
			'entry_num':  entry_num,
			}
		path = os.path.join(os.path.dirname(__file__), 'spider.html')
		self.response.out.write(template.render(path, template_values))

class Spider(webapp.RequestHandler):
	def post(self):
		weburl = WebUrl()
		weburl.url = self.request.get('start_url')
		weburl.info = web_spider.engine(weburl.url)
		#weburl.info = "no info"
		weburl.put()
		#print "no redirect"
		self.redirect('/spiderpage')

class Ti3Page(webapp.RequestHandler):
	def get(self):
		ti3match_query = Ti3Match.all().order('-date')
		recent_ti3match = ti3match_query.fetch(5)
		logged = 'false'
		if users.get_current_user():
			logged = 'true'
		main_link = '/'
		main_link_text = "Home Page"
		#global_stat = stats.GlobalStat.all().get()
		#total_bytes = global_stat.bytes
		#entry_num = global_stat.count
		total_bytes = 0
		entry_num = 0
		template_values = {
			'recent_ti3match': recent_ti3match,
			'logged': logged,
			'main_link_text': main_link_text,
			'main_link': main_link,
			'total_bytes': total_bytes,
			'entry_num':  entry_num,
		}
		path = os.path.join(os.path.dirname(__file__), 'ti3_gen.html')
		self.response.out.write(template.render(path, template_values))

class Ti3(webapp.RequestHandler):
	def post(self):
		ti3match = Ti3Match()
		players_number_string = self.request.get('player_number_string')
		ti3match.number_of_players = players_number_string
		#players_number = int(players_number_string)
		#ti3match.teams_assigned = TI3_player_gen_for_Web.engine(players_number)
		ti3match.teams_assigned = TI3_player_gen_for_Web.engine(players_number_string)
		ti3match.info = "no info"
		ti3match.put()
		# print "no redirect"
		self.redirect('/ti3page')

# The function run_wsgi_app() takes a WSGIApplication instance 
# (or another WSGI-compatible application object) and runs it
# in App Engine's CGI environment. 
# run_wsgi_app() is similar to the WSGI-to-CGI adaptor provided 
# by the wsgiref module in the Python standard library, but 
# includes a few additional features. 
# For example, it can automatically detect whether the application 
# is running in the development server or on App Engine, and 
# display errors in the browser if it is running on the development server.

application = webapp.WSGIApplication([
	('/', MainPage),
	('/spiderpage', SpiderPage),
	('/sign', Guestbook),
	('/spider', Spider),
	('/ti3', Ti3),
	('/ti3page', Ti3Page)],
	debug=True)

def main():
		run_wsgi_app(application)

if __name__ == "__main__":
	main()
