from sqlalchemy import Column, ForeignKey, String, Integer, Float, Boolean
from flask_sqlalchemy import SQLAlchemy
database_name = "TODO"
database_path = "postgresql://{}:{}@{}/{}".format('postgres', '123', 'localhost:5432', database_name)
database_path = "postgresql://cmsrraognpmaqi:413c93c2cabff045b2bb6910aa152d4f611d582cffa2f1652701518a8d4f1189@ec2-107-23-76-12.compute-1.amazonaws.com:5432/dehkajpu6edohp"
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    
    
'''
Films

'''

# Films = db.Table('films', 
#                 db.Column('actor_id',db.Integer, db.ForeignKey('actors.id'), primary_key = True),
#                 db.Column('movie_id',db.Integer, db.ForeignKey('movies.id'), primary_key = True)
#               )

class Films(db.Model):
  __tablename__ = 'films'
  id = Column(Integer, primary_key=True, default = 1, nullable= False)
  actor_id = Column(Integer, ForeignKey('actors.id'), primary_key = True)
  movie_id = Column(Integer, ForeignKey('movies.id'), primary_key = True)
  def __init__(self,id ,actor_id, movie_id):
    self.id = id
    self.actor_id = actor_id
    self.movie_id = movie_id
    
  def insert(self):
    db.session.add(self)
    db.session.commit()
    
  def update(self):
    db.session.commit()
    
  def delete(self):
    db.session.delete(self)
    db.session.commit()
    
  def format(self):
    return {
      'id': self.id,
      'actorId': self.actor_id,
      'movieId': self.movie_id,
    }
'''
Movies

'''
class Movies(db.Model):  
  __tablename__ = 'movies'

  id = Column(Integer, primary_key=True, default = 1, nullable= False)
  #public info
  title = Column(String(50))
  release_date = Column(String(8), default = '--/--/--')
  
  def __init__(self,id ,title, release_date):
    self.id = id
    self.title = title
    self.release_date = release_date

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'title': self.title,
      'releaseDate': self.release_date,
    }
    
'''
Actors

'''
class Actors(db.Model):  
  __tablename__ = 'actors'

  id = Column(Integer, primary_key=True, default = 1, nullable= False)
  #public info
  name = Column(String)
  age = Column(String)
  gender = Column(String)
  # movie_id = db.relationship('Movies',secondary = Films, backref=db.backref('Actors', lazy=True))

  def __init__(self, id, name , age, gender):
   self.id = id
   self.name = name
   self.age = age 
   self.gender = gender
   
  def insert(self):
   db.session.add(self)
   db.session.commit()
  
  def update(self):
   db.session.commit()

  def delete(self):
   db.session.delete(self)
   db.session.commit()

  def format(self):
   return {
      'id': self.id,
      'name': self.name,
      'age': self.age,
      'gender': self.gender
   }
