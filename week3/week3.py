from google.appengine.ext import ndb
import webapp2
import json

class Slip(ndb.Model):
	id = ndb.StringProperty()
	number = ndb.IntegerProperty(required=True)
	current_boat = ndb.StringProperty()
	arrival_date = ndb.StringProperty()
	departure_history = ndb.JsonProperty(repeated=True)

class Boat(ndb.Model):
	id = ndb.StringProperty()
	name = ndb.StringProperty(required=True)
	type = ndb.StringProperty()
	length = ndb.IntegerProperty()
	at_sea = ndb.BooleanProperty()

class SlipHandler(webapp2.RequestHandler):
	def post(self):
		slip_data = json.loads(self.request.body)
		if 'number' in slip_data:
			if slip_data['number']:
				new_slip = Slip(number=slip_data['number'], current_boat=None, arrival_date=None, departure_history=[])
				new_slip.put()
				new_slip.id = new_slip.key.urlsafe()
				new_slip.put()
				slip_dict = new_slip.to_dict()
				slip_dict['self'] = "/slips/" + new_slip.id
				self.response.write(json.dumps(slip_dict))
			else:
				self.response.set_status(400)
				return
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
				return
		else:
			query = Slip.query().fetch()
			slip_array = []
			for slip in query:
				current = {}
				current['id'] = slip.id
				current['number'] = slip.number
				current['current_boat'] = slip.current_boat
				current['arrival_date'] = slip.arrival_date
				current['self'] = '/slips/' + slip.id
				slip_array.append(current)
				
			self.response.write(json.dumps(slip_array))
	
	def delete(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			if slip:
				if slip.current_boat:
					boat_key = slip.current_boat
					boat = ndb.Key(urlsafe=boat_key).get()
					boat.at_sea = True
					boat.put()
				slip.key.delete()
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(404)
	
	def patch(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			if slip:
				slip_data = json.loads(self.request.body)
				if 'number' in slip_data:
					if slip_data['number']:
						slip.number = slip_data['number']
					else:
						self.response.set_status(400)
						return
				if 'current_boat' in slip_data:
					if slip.current_boat:
						old_boat_key = slip.current_boat
						old_boat = ndb.Key(urlsafe=old_boat_key).get()
						old_boat.at_sea = True
						old_boat.put()
					slip.current_boat = slip_data['current_boat']
				if 'arrival_date' in slip_data:
					slip.arrival_date = slip_data['arrival_date']
				slip.put()
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(404)
	
	def put(self, id=None):
		if id:
			slip_data = json.loads(self.request.body)
			if 'number' in slip_data:
				if slip_data['number']:
					slip = ndb.Key(urlsafe=id).get()
					if slip:
						if ('arrival_date' in slip_data and not 'current_boat' in slip_data) or (not 'arrival_date' in slip_data and 'current_boat' in slip_data):
							self.reponse.set_status(400)
						else:
							if slip.current_boat:
								old_boat_key = slip.current_boat
								old_boat = ndb.Key(urlsafe=old_boat_key).get()
								old_boat.at_sea = True
								old_boat.put()
							if 'arrival_date' in slip_data and 'current_boat' in slip_data:
								slip.arrival_date = slip_data['arrival_date']
								slip.current_boat = slip_data['current_boat']
							else:
								slip.arrival_date = None
								slip.current_boat = None
							slip.number = slip_data['number']
							slip.departure_history = []
							slip.put()
					else:
						self.response.set_status(404)
						return
				else:
					self.response.set_status(400)
					return
			else:
				self.response.set_status(400)
				return
		else:
			self.response.set_status(404)

class BoatHandler(webapp2.RequestHandler):
	def post(self):
		boat_data = json.loads(self.request.body)
		if 'name' in boat_data:
			if boat_data['name']:
				new_boat = Boat(name=boat_data['name'], at_sea=True)
				if 'type' in boat_data:
					new_boat.type = boat_data['type']
				else:
					new_boat.type = None
				if 'length' in boat_data:
					new_boat.length = boat_data['length']
				else:
					new_boat.length = None
				new_boat.put()
				new_boat.id = new_boat.key.urlsafe()
				new_boat.put()
				boat_dict = new_boat.to_dict()
				boat_dict['self'] = "/boats/" + new_boat.id
				self.response.write(json.dumps(boat_dict))
			else:
				self.response.set_status(400)
				return
		else:
			self.response.set_status(400)
	
	def get(self, id=None):
		if id:
			boat = ndb.Key(urlsafe=id).get()
			if boat:
				boat_dict = boat.to_dict()
				boat_dict['self'] = "/boats/" + id
				self.response.write(json.dumps(boat_dict))
			else:
				self.response.set_status(404)
				return
		else:
			query = Boat.query().fetch()
			boat_array = []
			for boat in query:
				current = {}
				current['id'] = boat.id
				current['name'] = boat.name
				current['type'] = boat.type
				current['length'] = boat.length
				current['at_sea'] = boat.at_sea
				current['self'] = '/boats/' + boat.id
				boat_array.append(current)
				
			self.response.write(json.dumps(boat_array))
	
	def delete(self, id=None):
		if id:
			boat = ndb.Key(urlsafe=id).get()
			if boat:
				if not boat.at_sea:
					query = Slip.query(Slip.current_boat == id)
					slip = query.get()
					slip.current_boat = None
					slip.arrival_date = None
					slip.put()
				boat.key.delete()
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(404)
	
	def patch(self, id=None):
		if id:
			boat = ndb.Key(urlsafe=id).get()
			if boat:
				boat_data = json.loads(self.request.body)
				if 'name' in boat_data:
					if boat_data['name']:
						boat.name = boat_data['name']
					else:
						self.response.set_status(400)
						return
				if  'type' in boat_data:
					boat.type = boat_data['type']
				if 'length' in boat_data:
					boat.length = boat_data['length']
				boat.put()
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(404)
	
	def put(self, id=None):
		if id:
			boat_data = json.loads(self.request.body)
			if 'name' in boat_data:
				if boat_data['name']:
					boat = ndb.Key(urlsafe=id).get()
					if boat:
						if 'name' in boat_data:
							boat.name = boat_data['name']
						else:
							self.response.set_status(400)
							return
						if 'type' in boat_data:
							boat.type = boat_data['type']
						else:
							boat.type = None
						if 'length' in boat_data:
							boat.length = boat_data['length']
						else:
							boat.length = None
						boat.put()
					else:
						self.response.set_status(404)
						return
				else:
					self.response.set_status(400)
					return
			else:
				self.response.set_status(400)
				return
		else:
			self.response.set_status(404)

class SlipHandler2(webapp2.RequestHandler):
	def get(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			if slip.current_boat:
				boat = ndb.Key(urlsafe=slip.current_boat).get()
				boat_dict = boat.to_dict()
				boat_dict['self'] = '/boats/' + boat.id
				self.response.write(json.dumps(boat_dict))
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(404)
	
	def put(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			if slip:
				if slip.current_boat:
					self.response.set_status(400)
					return
				else:
					slip_data = json.loads(self.request.body)
					if 'id' in slip_data and 'arrival_date' in slip_data:
						slip.current_boat = slip_data['id']
						slip.arrival_date = slip_data['arrival_date']
						slip.put()
						boat = ndb.Key(urlsafe=slip_data['id']).get()
						boat.at_sea = False
						boat.put()
					else:
						self.response.set_status(400)
						return
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(404)
	
	def patch(self, id=None):
		if id:
			slip = ndb.Key(urlsafe=id).get()
			if slip.current_boat:
				boat = ndb.Key(urlsafe=slip.current_boat).get()
				if slip and boat:
					slip_data = json.loads(self.request.body)
					if 'departure_date' in slip_data:
						hist_dict = {}
						hist_dict['departure_date'] = slip_data['departure_date']
						hist_dict['departed_boat'] = boat.id
						slip.departure_history.append(json.dumps(hist_dict))
					boat.at_sea = True
					boat.put()
					slip.current_boat = None
					slip.arrival_date = None
					slip.put()
				else:
					self.response.set_status(404)
					return
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(404)

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write("Sammy Pettinichi's CS496 REST Planning and Implementation Project")

allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
	('/', MainPage),
	('/boats', BoatHandler),
	('/boats/(.*)', BoatHandler),
	('/slips/(.*)/boat', SlipHandler2),
	('/slips', SlipHandler),
	('/slips/(.*)', SlipHandler),
], debug=True)