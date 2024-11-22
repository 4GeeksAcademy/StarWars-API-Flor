from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    name = db.Column(db.String(200), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    population = db.Column(db.Integer)
    weather = db.Column (db.String(50), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "population": self.population,
            "name": self.name,
            "weather": self.weather,
        }

class People(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    zodiac = db.Column (db.String(100))

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "age": self.age,
            "name": self.name,
            "zodiac": self.zodiac,
        }

class Favorite(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    people = db.relationship(People)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)

    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        people = People.query.filter_by(id=self.people_id).first()
        planet = Planet.query.filter_by(id=self.planet_id).first()
        user = User.query.filter_by(id=self.user_id).first()
        return {
            "id": self.id,
            "people_id": people.serialize() if people else None,
            # "people_id": self.people.serialize() if self.people != None else "",
            "user_id": user.serialize() if user else None,
            # "user_id": self.user.serialize() if self.user != None else "",
            "planet_id": planet.serialize() if planet else None,
            # "planet_id": self.planet.serialize() if self.planet != None else "",
        }
