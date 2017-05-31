CLIENT_ID = '367748320634-vdkilqrod6apumrmfpnb11esmvbc09te.apps.googleusercontent.com'
CLIENT_SECRET = '9WIFcgdJIS-UQ4X0gLfwSyBq'
GOOGLE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
REDIRECT_URL = 'https://cs496-final-project-168900.appspot.com/callback'


import os
import httplib, urllib
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb
from oauth2client import client, crypt
import webapp2
import json
import jinja2
import string
import random
import logging

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
		
		token = r['id_token']
		
		template_values = {
			'token_info': token
		}
		
		template = JINJA_ENVIRONMENT.get_template('callback.html')
		self.response.write(template.render(template_values))

def getParentKey(userid):
	if userid is not None:
		parent_key = ndb.Key(Wedding, repr(userid))
		return parent_key
	else:
		return None

def parseToken(token):
	if token is not None:
		try:
			idinfo = client.verify_id_token(token, None)
			if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
				raise crypt.AppIdentityError("Wrong issuer.")
			if idinfo['aud'] not in [CLIENT_ID]:
				raise crypt.AppIdentityError("Unrecognized client.")
			userid = idinfo['sub']
			return userid
		except crypt.AppIdentityError:
			return None
	else:
		return None

class Wedding(ndb.Model):
	id = ndb.StringProperty()
	token_id = ndb.StringProperty(required=True)
	person1 = ndb.StringProperty()
	person2 = ndb.StringProperty()
	date = ndb.StringProperty()
	venue = ndb.StringProperty()

class Person(ndb.Model):
	id = ndb.StringProperty()
	token_id = ndb.StringProperty(required=True)
	name = ndb.StringProperty(required=True)
	spouse = ndb.StringProperty()
	hometown = ndb.StringProperty()
	age = ndb.IntegerProperty()

class PersonHandler(webapp2.RequestHandler):
	def post(self):
		if 'token_id' in self.request.headers:
			token = self.request.headers['token_id']
			header_data = parseToken(token)
		else:
			self.response.set_status(403)
			return
		person_data = json.loads(self.request.body)
		if header_data and 'name' in person_data:
			if person_data['name']:
				new_person = Person(parent=getParentKey(header_data),token_id=header_data,name=person_data['name'],spouse=None,hometown=None,age=None)
				if 'spouse' in person_data:
					new_person.spouse = person_data['spouse']
				if 'hometown' in person_data:
					new_person.hometown = person_data['hometown']
				if 'age' in person_data:
					new_person.age = person_data['age']
				new_person.put()
				new_person.id = new_person.key.urlsafe()
				new_person.put()
				person_dict = new_person.to_dict()
				person_dict['self'] = "/people/" + new_person.id
				self.response.write(json.dumps(person_dict))
			else:
				self.response.set_status(400)
				return
		else:
			self.response.set_status(400)
			return
	
	def get(self, id=None):
		if 'token_id' in self.request.headers:
			header_data = parseToken(self.request.headers['token_id'])
		else:
			self.response.set_status(400)
			return
		if header_data:
			if id:
				person = ndb.Key(urlsafe=id).get()
				if person:
					if person.token_id == header_data:
						person_dict = person.to_dict()
						person_dict['self'] = "/people/" + person.id
						self.response.write(json.dumps(person_dict))
					else:
						self.response.set_status(403)
						return
				else:
					self.response.set_status(404)
					return
			else:
				parent_key = getParentKey(header_data)
				people = Person.query(ancestor=parent_key).fetch()
				if people:
					person_array = []
					for person in people:
						current = {}
						current['id'] = person.id
						current['name'] = person.name
						current['spouse'] = person.spouse
						current['hometown'] = person.hometown
						current['age'] = person.age
						current['self'] = "/people/" + person.id
						person_array.append(current)
					self.response.write(json.dumps(person_array))
				else:
					self.response.set_status(404)
					return
		else:
			self.response.set_status(400)
			return
	
	def put(self, id=None):
		if id:
			if 'token_id' in self.request.headers:
				header_data = parseToken(self.request.headers['token_id'])
			else:
				self.response.set_status(400)
				return
			person_data = json.loads(self.request.body)
			person = ndb.Key(urlsafe=id).get()
			if person:
				if header_data == person.token_id:
					if 'name' in person_data and person_data['name']:
						person.name = person_data['name']
						if 'spouse' in person_data:
							person.spouse = person_data['spouse']
						else:
							person.spouse = None
						if 'hometown' in person_data:
							person.hometown = person_data['hometown']
						else:
							person.hometown = None
						if 'age' in person_data:
							person.age = person_data['age']
						else:
							person.age = None
					else:
						self.response.set_status(400)
				else:
					self.response.set_status(403)
			else:
				self.response.set_status(404)
		else:
			self.response.set_status(400)
	
	def patch(self, id=None):
		if id:
			if 'token_id' in self.request.headers:
				header_data = parseToken(self.request.headers['token_id'])
			else:
				self.response.set_status(400)
				return
			person_data = json.loads(self.request.body)
			person = ndb.Key(urlsafe=id).get()
			if person:
				if header_data == person.token_id:
					if 'name' in person_data and person_data['name']:
						person.name = person_data['name']
					if 'spouse' in person_data:
						person.spouse = person_data['spouse']
					if 'hometown' in person_data:
						person.hometown = person_data['hometown']
					if 'age' in person_data:
						person.age = person_data['age']
				else:
					self.response.set_status(403)
			else:
				self.response.set_status(404)
		else:
			self.response.set_status(400)
	
	def delete(self, id=None):
		if id:
			if 'token_id' in self.request.headers:
				header_data = parseToken(self.request.headers['token_id'])
			else:
				self.response.set_status(400)
				return
			person = ndb.Key(urlsafe=id).get()
			if person:
				if header_data == person.token_id:
					query1 = Wedding.query(Wedding.person1 == id).get()
					query2 = Wedding.query(Wedding.person2 == id).get()
					query3 = Person.query(Person.spouse == id).get()
					if query1:
						query1.person1 = None
						query1.put()
					if query2:
						query2.person2 = None
						query2.put()
					if query3:
						query3.spouse = None
						query3.put()
					person.key.delete()
				else:
					self.response.set_status(403)
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(400)
			return

class WeddingHandler(webapp2.RequestHandler):
	def post(self):
		if 'token_id' in self.request.headers:
			token = self.request.headers['token_id']
			header_data = parseToken(token)
		else:
			self.response.set_status(403)
			return
		wedding_data = json.loads(self.request.body)
		if header_data:
			if header_data:
				new_wedding = Wedding(parent=getParentKey(header_data),token_id=header_data,person1=None,person2=None,date=None,venue=None)
				if 'person1' in wedding_data:
					new_wedding.person1 = wedding_data['person1']
				if 'person2' in wedding_data:
					new_wedding.person1 = wedding_data['person2']
				if 'date' in wedding_data:
					new_wedding.date = wedding_data['date']
				if 'venue' in wedding_data:
					new_wedding.venue = wedding_data['venue']
				new_wedding.put()
				new_wedding.id = new_wedding.key.urlsafe()
				new_wedding.put()
				wedding_dict = new_wedding.to_dict()
				wedding_dict['self'] = "/weddings/" + new_wedding.id
				self.response.write(json.dumps(wedding_dict))
			else:
				self.response.set_status(400)
				return
		else:
			self.response.set_status(400)
			return
	
	def get(self, id=None):
		if 'token_id' in self.request.headers:
			header_data = parseToken(self.request.headers['token_id'])
		else:
			self.response.set_status(400)
			return
		if header_data:
			if id:
				wedding = ndb.Key(urlsafe=id).get()
				if wedding:
					if wedding.token_id == header_data:
						wedding_dict = wedding.to_dict()
						wedding_dict['self'] = "/weddings/" + id
						self.response.write(json.dumps(wedding_dict))
					else:
						self.response.set_status(403)
						return
				else:
					self.response.set_status(404)
					return
			else:
				parent_key = getParentKey(header_data)
				wedding = Wedding.query(ancestor=parent_key).fetch()
				if wedding:
					wedding_dict = wedding.to_dict()
					wedding_dict['self'] = "/weddings/" + id
					self.response.write(json.dumps(wedding_dict))
				else:
					self.response.set_status(404)
					return
		else:
			self.response.set_status(400)
			return
	
	def put(self, id=None):
		if id:
			if 'token_id' in self.request.headers:
				header_data = parseToken(self.request.headers['token_id'])
			else:
				self.response.set_status(400)
				return
			wedding_data = json.loads(self.request.body)
			wedding = ndb.Key(urlsafe=id).get()
			if wedding:
				if header_data == wedding.token_id:
					if 'person1' in wedding_data:
						wedding.person1 = wedding_data['person1']
					else:
						wedding.person1 = None
					if 'person2' in wedding_data:
						wedding.person2 = wedding_data['person2']
					else:
						wedding.person2 = None
					if 'venue' in wedding_data:
						wedding.venue = wedding_data['venue']
					else:
						wedding.venue = None
					if 'date' in wedding_data:
						wedding.date = wedding_data['date']
					else:
						wedding.date = None
					wedding.put()
				else:
					self.response.set_status(403)
			else:
				self.response.set_status(404)
				return
		else:
			self.reponse.set_status(400)
			return
	
	def patch(self, id=None):
		if id:
			if 'token_id' in self.request.headers:
				header_data = parseToken(self.request.headers['token_id'])
			else:
				self.response.set_status(400)
				return
			wedding_data = json.loads(self.request.body)
			wedding = ndb.Key(urlsafe=id).get()
			if wedding:
				if header_data == wedding.token_id:
					if 'person1' in wedding_data:
						wedding.person1 = wedding_data['person1']
					if 'person2' in wedding_data:
						wedding.person2 = wedding_data['person2']
					if 'venue' in wedding_data:
						wedding.venue = wedding_data['venue']
					if 'date' in wedding_data:
						wedding.date = wedding_data['date']
					wedding.put()
				else:
					self.response.set_status(403)
			else:
				self.response.set_status(404)
				return
		else:
			self.reponse.set_status(400)
			return
	
	def delete(self, id=None):
		if id:
			if 'token_id' in self.request.headers:
				header_data = parseToken(self.request.headers['token_id'])
			else:
				self.response.set_status(400)
				return
			wedding = ndb.Key(urlsafe=id).get()
			if wedding:
				if header_data == wedding.token_id:
					wedding.key.delete()
				else:
					self.response.set_status(403)
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(400)
			return

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
	('/callback', CallbackHandler),
	('/weddings', WeddingHandler),
	('/weddings/(.*)', WeddingHandler),
	('/people', PersonHandler),
	('/people/(.*)', PersonHandler)
], debug=True)