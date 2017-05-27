from google.appengine.ext import ndb
import webapp2
import json

class Favorites(ndb.Model):
	id = ndb.StringProperty()
	google_id = ndb.StringProperty(required=True)
	color = ndb.StringProperty()
	season = ndb.StringProperty()
	movie = ndb.StringProperty()
	superhero = ndb.StringProperty()

class FavHandler(webapp2.RequestHandler):
	def post(self):
		fav_data = json.loads(self.request.body)
		if 'google_id' in fav_data:
			if fav_data['google_id']:
				new_fav = Favorites(google_id=fav_data['google_id'],color=None, season=None, movie=None, superhero=None)
				if 'color' in fav_data:
					new_fav.color = fav_data['color']
				if 'season' in fav_data
					new_fav.season = fav_data['season']
				if 'movie' in fav_data:
					new_fav.movie = fav_data['movie']
				if 'superhero' in fav_data:
					new_fav.superhero = fav_data['superhero']
				new_fav.put()
				new_fav.id = new_slip.key.urlsafe()
				new_fav.put()
				fav_dict = new_fav.to_dict()
				fav_dict['self'] = "/users/" + new_fav.id
				self.response.write(json.dumps(fav_dict))
			else:
				self.response.set_status(400)
				return
		else:
			self.response.set_status(400)
			return
	
	def get(self, id=None):
		if id:
			fav = ndb.Key(urlsafe=id).get()
			if fav:
				fav_dict = fav.to_dict()
				fav_dict['self'] = "/users/" + id
				self.response.write(json.dumps(fav_dict))
			else:
				self.response.set_status(404)
				return
		else:
			self.response.set_status(400)
			return
	
	def put(self, id=None):
		if id:
			fav = ndb.Key(urlsafe=id).get()
			if fav:
				if 'color' in fav_data:
					if fav_data['color']:
						fav.color = fav_data['color']
					else:
						self.reponse.set_status(400)
						return
				else:
					fav.color = None
				if 'season' in fav_data
					if fav_data['season']:
						fav.season = fav_data['season']
					else:
						self.reponse.set_status(400)
						return
				else:
					fav.season = None
				if 'movie' in fav_data:
					if fav_data['movie']:
						fav.movie = fav_data['movie']
					else:
						self.reponse.set_status(400)
						return
				else:
					fav.movie = None
				if 'superhero' in fav_data:
					if fav_data['superhero']:
						fav.superhero = fav_data['superhero']
					else:
						self.reponse.set_status(400)
						return
				else:
					fav.superhero = None
				fav.put()
			else:
				self.response.set_status(404)
				return
		else:
			self.reponse.set_status(400)
			return
	
	def patch(self, id=None):
		if id:
			fav = ndb.Key(urlsafe=id).get()
			if fav:
				if 'color' in fav_data:
					if fav_data['color']:
						fav.color = fav_data['color']
					else:
						self.reponse.set_status(400)
						return
				if 'season' in fav_data
					if fav_data['season']:
						fav.season = fav_data['season']
					else:
						self.reponse.set_status(400)
						return
				if 'movie' in fav_data:
					if fav_data['movie']:
						fav.movie = fav_data['movie']
					else:
						self.reponse.set_status(400)
						return
				if 'superhero' in fav_data:
					if fav_data['superhero']:
						fav.superhero = fav_data['superhero']
					else:
						self.reponse.set_status(400)
						return
				fav.put()
			else:
				self.response.set_status(404)
				return
		else:
			self.reponse.set_status(400)
			return
	
	def delete(self, id=None):
		if id:
			fav = ndb.Key(urlsafe=id).get()
			if fav:
				fav.key.delete()
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
	('/users', FavHandler),
	('/users/(.*)', FavHandler)
], debug=True)