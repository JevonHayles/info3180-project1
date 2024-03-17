from . import db
from werkzeug.security import generate_password_hash

class PropertyProfile(db.Model):
    __tablename__ = 'property_profiles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    description = db.Column(db.String(500))
    num_rooms = db.Column(db.Integer)
    num_bathrooms = db.Column(db.Integer)
    price = db.Column(db.Integer)
    prop_type = db.Column(db.String(10))
    location = db.Column(db.String(150))
    photo = db.Column(db.String(150))

    def __init__(self, title, description, num_rooms, num_bathrooms, price, prop_type, location, photo):
        self.title = title
        self.description = description
        self.num_rooms = num_rooms
        self.num_bathrooms = num_bathrooms
        self.price = price
        self.prop_type = prop_type
        self.location = location
        self.photo = photo

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support  
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<Property %r>' % (self.username)