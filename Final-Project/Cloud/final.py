import os
from google.appengine.ext import ndb
import webapp2
import json
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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
	hometown = ndb.StringProperty
	age = ndb.IntegerProperty()

class PersonHandler(webapp2.RequestHandler):
	def post(self):
		person_data = json.loads(self.request.body)
		if 'token_id' in person_data and 'name' in person_data:
			if person_data['token_id'] and person_data['name']:
				new_person = Person(token_id=person_data['token_id'],name=person_data['name'],spouse=None,hometown=None,age=None)
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
		header_data = json.loads(self.request.headers)
		if 'token_id' in header_data:
			if id:
				person = ndb.Key(urlsafe=id).get()
				if person:
					if person.token_id == header_data['token_id']:
						person_dict = person.to_dict()
						person_dict['self'] = "/people/" + person.id
						self.response.write(json.dumps(person_dict))
					else:
						self.response.set_status(400)
						return
				else:
					self.response.set_status(404)
					return
			else:
				person = Person.query(Person.token_id == header_data['token_id']).get()
				if person:
					person_dict = person.to_dict()
					person_dict['self'] = "/people/" + person.id
					self.response.write(json.dumps(person_dict))
				else:
					self.response.set_status(404)
					return
		else:
			self.response.set_status(400)
			return
	
	def put(self, id=None):
		if id:
			person_data = json.loads(self.reques.body)
			person = ndb.Key(urlsafe=id).get()
			if person:
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
				self.response.set_status(404)
		else:
			self.response.set_status(400)
	
	def patch(self, id=None):
		if id:
			person_data = json.loads(self.reques.body)
			person = ndb.Key(urlsafe=id).get()
			if person:
				if 'name' in person_data and person_data['name']:
					person.name = person_data['name']
				if 'spouse' in person_data:
					person.spouse = person_data['spouse']
				if 'hometown' in person_data:
					person.hometown = person_data['hometown']
				if 'age' in person_data:
					person.age = person_data['age']
				else:
					self.response.set_status(400)
			else:
				self.response.set_status(404)
		else:
			self.response.set_status(400)
	
	def delete(self, id=None):
		if id:
			person = ndb.Key(urlsafe=id).get()
			if person:
				query1 = Wedding.query(Wedding.person1 == id).get()
				query2 = Wedding.query(Wedding.person2 == id).get()
				if query1:
					query1.person1 = None
					query1.put()
				if query2:
					query2.person2 = None
					query2.put()
				person.key.delete()
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(400)
			return

class WeddingHandler(webapp2.RequestHandler):
	def post(self):
		wedding_data = json.loads(self.request.body)
		if 'token_id' in wedding_data:
			if wedding_data['token_id']:
				new_wedding = Wedding(token_id=wedding_data['token_id'],person1=None,person2=None,date=None,venue=None)
				if 'person1' in wedding_data:
					new_wedding.person1 = wedding_data['person1']
				if 'person2' in wedding_data:
					new_wedding.person1 = wedding_data['person2']
				if 'date' in wedding_data:
					new_wedding.date = wedding_data['date']
				if 'venue' in wedding_data:
					new_wedding.movie = wedding_data['venue']
				new_wedding.put()
				new_wedding.id = new_slip.key.urlsafe()
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
		header_data = json.loads(self.request.headers)
		if 'token_id' in header_data:
			if id:
				wedding = ndb.Key(urlsafe=id).get()
				if wedding:
					if wedding.token_id == header_data['token_id']:
						wedding_dict = wedding.to_dict()
						wedding_dict['self'] = "/weddings/" + id
						self.response.write(json.dumps(wedding_dict))
					else:
						self.response.set_status(400)
						return
				else:
					self.response.set_status(404)
					return
			else:
				wedding = Wedding.query(Wedding.token_id == header_data['token_id']).get()
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
			wedding_data = json.loads(self.request.body)
			wedding = ndb.Key(urlsafe=id).get()
			if wedding:
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
				self.response.set_status(404)
				return
		else:
			self.reponse.set_status(400)
			return
	
	def patch(self, id=None):
		if id:
			wedding = ndb.Key(urlsafe=id).get()
			if wedding:
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
				self.response.set_status(404)
				return
		else:
			self.reponse.set_status(400)
			return
	
	def delete(self, id=None):
		if id:
			wedding = ndb.Key(urlsafe=id).get()
			if wedding:
				wedding.key.delete()
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(400)
			return

class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render())
		#self.response.write("Sammy Pettinichi's CS496 Final Project")

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/weddings', WeddingHandler),
	('/weddings/(.*)', WeddingHandler),
	('/people', PersonHandler),
	('/people/(.*)', PersonHandler)
], debug=True)