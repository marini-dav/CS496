from google.appengine.ext import ndb
import webapp2
import json

class Slip(ndb.Model):
	id = ndb.StringProperty()
	number = ndb.IntegerProperty(required=True)
	current_boat = ndb.StringProperty()
	arrival_date = ndb.StringProperty()
	departure_history = ndb.StringProperty()

class Ship(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty(required=True)
	type = ndb.StringProperty()
	length = ndb.IntegerProperty()
	at_sea = ndb.BooleanProperty()

class SlipHandler(webapp2.RequestHandler):
	def post(self):
		slip_data = json.loads(self.request.body)
		if slip_data['number']:
			new_slip = Slip(number=slip_data['number'], current_boat=None, arrival_date=None)
			new_slip.put()
			new_slip.id = new_slip.key.urlsafe()
			new_slip.put()
			slip_dict = new_slip.to_dict()
			slip_dict['self'] = '/slips/' + new_slip.key.urlsafe()
			self.response.write(json.dumps(slip_dict))
		else:
			self.response.set_status(400)
	
	def get(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			if slip:
				slip_dict = slip.to_dict()
				slip_dict['self'] = "/slips/" + id
				self.response.write(json.dumps(slip_dict))
			else:
				self.response.set_status(404)
		else:
			slips = Ship.query().fetch()
			self.response.write(slips)
	
	def delete(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			if slip:
				if slip.current_boat:
					ship = ndb.Key(urlsafe=slip.current_boat).get()
					ship.at_sea = True
					ship.put()
				slip.key.delete()
			else:
				self.response.set_status(404)
	
	def patch(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			if slip:
				slip_data = json.loads(self.request.body)
				if slip_data['number']:
					slip.number = slip_data['number']
				if  slip_data['current_boat']:
					slip.current_boat = slip_data['current_boat']
				if slip_data['arrival_date']:
					slip.arrival_date = slip_data['arrival_date']
				slip.put()
			else:
				self.response.set_status(404)
	
	def put(self, id=None):
		if id:
			slip_data = json.loads(self.request.body)
			slip = ndb.Key(urlsafe=id).get()
			if slip:
				old_boat_key = slip.current_boat
				old_boat = ndb.Key(urlsafe=old_boat_key)
				old_boat.at_sea = True
				slip.number = slip_data['number']
				slip.current_boat = slip_data['current_boat']
				slip.arrival_date = slip_data['arrival_date']
				slip.put()
				slip_dict = slip.to_dict()
				slip_dict['self'] = '/slips/' + slip.key.urlsafe()
				self.response.write(json.dumps(slip_dict))
			else:
				self.response.set_status(404)

class ShipHandler(webapp2.RequestHandler):
	def post(self):
		ship_data = json.loads(self.request.body)
		if ship_data['name']:
			new_ship = Ship(name=ship_data['name'], at_sea=True)
			if ship_data['type']:
				new_ship.type = ship_data['type']
			if ship_data['length']:
				new_ship.length = ship_data['length']
			new_ship.put()
			new_ship.id = new_ship.key.urlsafe()
			new_ship.put()
			ship_dict = new_ship.to_dict()
			ship_dict['self'] = '/ships/' + new_ship.key.urlsafe()
			self.response.write(json.dumps(ship_dict))
		else:
			self.response.set_status(400)
	
	def get(self, id=None):
		if id:
			ship = ndb.Key(urlsafe=id).get()
			if ship:
				ship_dict = ship.to_dict()
				ship_dict['self'] = "/ships/" + id
				self.response.write(json.dumps(ship_dict))
			else:
				self.response.set_status(404)
		else:
			ships = Ship.query().fetch()
			self.response.write(ships)
	
	def delete(self, id=None):
		if id:
			ship = ndb.Key(urlsafe=id).get()
			if ship:
				ship_dict = ship.to_dict()
				if not ship_dict['at_sea']:
					slip = ndb.Key(urlsafe=id).get()
					slip.current_boat = None
					slip.put()
				ship.key.delete()
			else:
				self.response.set_status(404)
	
	def patch(self, id=None):
		if id:
			ship = ndb.Key(urlsafe=id).get()
			if ship:
				ship_data = json.loads(self.request.body)
				if ship_data['name']:
					ship.name = ship_data['name']
				if  ship_data['type']:
					ship.type = ship_data['type']
				if ship_data['length']:
					ship.length = ship_data['length']
				if ship_data['at_sea']:
					ship.at_sea = True
				ship.put()
			else:
				self.response.set_status(404)
	
	def put(self, id=None):
		if id:
			ship = ndb.Key(urlsafe=id).get()
			if ship:
				ship_data = json.loads(self.request.body)
				ship.name = ship_data['name']
				ship.type = ship_data['type']
				ship.length = ship_data['length']
				ship.put()
				ship_dict = ship.to_dict()
				ship_dict['self'] = '/ships/' + ship.key.urlsafe()
				self.response.write(json.dumps(ship_dict))
			else:
				self.response.set_status(404)

class SlipHandler2(webapp2.RequestHandler):
	def get(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			ship = ndb.Key(urlsafe=slip.current_boat).get()
			ship_dict = ship.to_dict()
			ship_dict['self'] = '/ships/' + new_ship.key.urlsafe()
			self.response.write(json.dumps(ship_dict))
			
	def put(self, id=None):
		if id:
			slip_data = json.loads(self.request.body)
			slip = ndb.Key(urlsafe=id).get()
			slip.current_boat = slip_data['id']
			slip.arrival_date = slip_data['arrival_date']
			slip.put()
	
	def delete(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			ship = ndb.Key(slip.current_boat).get()
			ship.at_sea = True
			ship.put()
			slip.current_boat = None
			slip.arrival_date = None
			slip.put()

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("hello")

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/ships', ShipHandler),
	('/ships/(.*)', ShipHandler),
	('/slips', SlipHandler),
	('/slips/(.*)', SlipHandler),
	('/slips/(.*)/ship', SlipHandler2)
], debug=True)