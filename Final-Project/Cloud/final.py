from google.appengine.ext import ndb
import webapp2
import json

class Wedding(ndb.Model):
	id = ndb.StringProperty()
	person1 = ndb.StringProperty()
	person2 = ndb.StringProperty()
	date = ndb.StringProperty()
	venue = ndb.StringProperty()

class Person(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty(required=True)
	parent1 = ndb.StringProperty()
	parent2 = ndb.StringProperty()
	age = ndb.IntegeProperty()

class PersonHandler(webapp2.RequestHandler):
	def post(self):
		person_data = json.loads(self.reques.body)
		if 'name' in person_data:
			if person_data['name']:
				new_person = Person(name=person_data['name'],parent1=None,parent2=None,age=None)
				if 'parent1' in person_data:
					new_person.parent1 = person_data['parent1']
				if 'parent2' in person_data:
					new_person.parent2 = person_data['parent2']
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
		if id:
			person = ndb.Key(urlsafe=id).get()
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
					if 'parent1' in person_data:
						person.parent1 = person_data['parent1']
					else:
						person.parent1 = None
					if 'parent2' in person_data:
						person.parent2 = person_data['parent2']
					else:
						person.parent2 = None
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
				if 'parent1' in person_data:
					person.parent1 = person_data['parent1']
				if 'parent2' in person_data:
					person.parent2 = person_data['parent2']
				if 'age' in person_data:
					person.age = person_data['age']
				else:
					self.response.set_status(400)
			else:
				self.response.set_status(404
		else:
			self.response.set_status(400)
	
	def delete(self, id=None):
		if id:
			person = ndb.Key(urlsafe=id).get()
			if person:
				query1 = Wedding.query(Wedding.person1 == id)
				query2 = Wedding.query(Wedding.person2 == id)
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
		if 'person1' in wedding_data or 'person2' in wedding_data:
			new_wedding = Wedding(person1=wedding_data['person1'],person2=wedding_data['person2'],date=None,venue=None)
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
	
	def get(self, id=None):
		if id:
			wedding = ndb.Key(urlsafe=id).get()
			if wedding:
				wedding_dict = wedding.to_dict()
				wedding_dict['self'] = "/users/" + id
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
					if wedding_data['person1']:
						wedding.person1 = wedding_data['person1']
					else:
						self.reponse.set_status(400)
						return
				else:
					wedding.person1 = None
				if 'person2' in wedding_data
					if wedding_data['person2']:
						wedding.person2 = wedding_data['person2']
					else:
						self.reponse.set_status(400)
						return
				else:
					wedding.person2 = None
				if 'venue' in wedding_data:
					if wedding_data['venue']:
						wedding.venue = wedding_data['venue']
					else:
						self.reponse.set_status(400)
						return
				else:
					wedding.venue = None
				if 'date' in wedding_data:
					if wedding_data['date']:
						wedding.date = wedding_data['date']
					else:
						self.reponse.set_status(400)
						return
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
				if 'person2' in wedding_data
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
		self.response.write("Sammy Pettinichi's CS496 Final Project")

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/weddings', weddingHandler),
	('/weddings/(.*)', weddingHandler),
	('/people', personHandler),
	('/people/(.*)', personHandler)
], debug=True)