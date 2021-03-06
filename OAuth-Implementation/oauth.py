CLIENT_ID = "822545719705-ai33lpgvdtj7o069r4krikae6s20r663.apps.googleusercontent.com"
CLIENT_SECRET = "XjwySGyHwuhOvAKkGMAPtZ_z"
GOOGLE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
REDIRECT_URL = "https://oauthimplementation-166521.appspot.com/callback"

import os
import httplib, urllib
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import webapp2
import json
import string
import random
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class State(ndb.Model):
	value = ndb.StringProperty(required=True)

def generate_state(length=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(length))

class CallbackHandler(webapp2.RequestHandler):
	def get(self,):
		state_return = self.request.get('state')
		code = self.request.get('code')
		
		query = State.query(State.value == state_return)
		current_state = query.get()
		if state_return != current_state.value:
			template = JINJA_ENVIRONMENT.get_template('failure.html')
			self.response.write(template.render())
			return
		current_state.key.delete()
		
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		payload = {'grant_type': 'authorization_code',
		'code': code,
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'redirect_uri': REDIRECT_URL}
		result = urlfetch.fetch(url='https://www.googleapis.com/oauth2/v4/token', headers=headers, payload=urllib.urlencode(payload), method=urlfetch.POST)
		r = json.loads(result.content)
		
		auth_key = "Bearer " + r['access_token']
		
		headers = {
			'Authorization': auth_key
		}
		response = urlfetch.fetch(url='https://www.googleapis.com/plus/v1/people/me', headers=headers, method=urlfetch.GET)
		r = json.loads(response.content)
		r_name = r['name']
		
		template_values = {
			'displayName': r['displayName'],
			'familyName': r_name['familyName'],
			'givenName': r_name['givenName'],
			'url': r['url'],
			'state': state_return
		}
		
		template = JINJA_ENVIRONMENT.get_template('callback.html')
		self.response.write(template.render(template_values))

class MainPage(webapp2.RequestHandler):
	def get(self):
		state = generate_state()
		new_state = State(value=state)
		new_state.put()
		url = GOOGLE_URL + "?response_type=code&client_id=" + CLIENT_ID + "&redirect_uri=" + REDIRECT_URL + "&scope=email&state=" + state
		template_values = {
			'url': url
		}
		
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/callback', CallbackHandler)
], debug=True)