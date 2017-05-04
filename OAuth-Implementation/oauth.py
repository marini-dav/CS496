CLIENT_ID = "822545719705-ai33lpgvdtj7o069r4krikae6s20r663.apps.googleusercontent.com"
CLIENT_SECRET = "XjwySGyHwuhOvAKkGMAPtZ_z"
GOOGLE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
REDIRECT_URL = "https://oauthimplementation-166521.appspot.com/callback"
state = ""

import os
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

def generate_state(length=10, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(length))

class CallbackHandler(webapp2.RequestHandler):
	def get(self,):
		state_return = self.request.get('state')
		code = self.request.get('code')
		
		#if state_return != state:
			
		
		payload = {'grant_type': 'authorization_code',
		'code': code,
		'client_id': CLIENT_ID,
		'client_secret': CLIENT_SECRET,
		'redirect_uri': REDIRECT_URL}
		result = json.loads(urlfetch.fetch(url='https://www.googleapis.com/oauth2/v4/token', payload = json.dumps(payload), method=urlfetch.POST).content)
		
		auth_key = "Bearer " + result['access_token']
		
		payload = {'Authorization': auth_key}
		response = json.loads(urlfetch.fetch(url='https://www.googleapis.com/plus/v1/people/me', payload = json.dumps(payload), method=urlfetch.GET).content)
		
		template_values = {
			'name': response.displayName,
			'url': response.url,
			'state': state
		}
		
		template = JINJA_ENVIRONMENT.get_template('callback.html')
		self.response.write(template.render(template_values))

class MainPage(webapp2.RequestHandler):
	def get(self):
		state = generate_state()
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