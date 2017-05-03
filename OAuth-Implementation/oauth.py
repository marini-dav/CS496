#import requests
#import requests.auth
import os
import urllib
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2
import json
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class CallbackHandler(webapp2.RequestHandler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name',
										  DEFAULT_GUESTBOOK_NAME)
		greetings_query = Greeting.query(
			ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(10)
		
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		
		template_values = {
			'user': user,
			'greetings': greetings,
			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
		}
		
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(values))

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render())

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/callback', CallbackHandler)
], debug=True)