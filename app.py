import json
import sys
from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from models import Movies, Actors, Films, setup_db
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth .auth import requires_auth

def find_missing_id(total_records = 0, id_list = []):
        #find sum of an N number
        total_sum_of_records = (total_records*(total_records + 1))/2
        total_sum_of_id_records = (len(id_list)*(len(id_list) + 1))/2
        if (total_sum_of_id_records == total_sum_of_records):
            #if there is not missing id return the next id in the range
            return len(id_list) + 1
        for item in id_list:
            total_sum_of_records -= item
        #if there is a missing id like 6 is missing from the  [1,2,3,4,5,7,8,9] 6 will be returned
        return total_sum_of_records

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  db = SQLAlchemy(app)
  CORS(app)
  @app.after_request
  def after_request(response):
    response.headers.add(
      "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
      "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS,PATCH"
    )
    return response

  @app.route('/movies', methods=['GET'])
  @requires_auth(permission = "get:movies")
  def get_movie_handler(payload):
    movie_list = []
    casted_actor_id_list = []
    actor_list = []
    try:
        searched_movie_name = request.args.get('movieName', '', str)
        if searched_movie_name != '':
          movie_list = Movies.query.filter(Movies.title.ilike(f'%{searched_movie_name}%')).all()
          if len(movie_list) == 0:
            abort(404)
        else:
          movie_list = Movies.query.all()
        movie_list = [Movies.format(item) for item in movie_list]
        for movie in movie_list:
          casted_actor_id_list = Films.query.filter_by(movie_id = movie["id"]).all()
          for item in casted_actor_id_list:
            actor_data = Actors.query.filter_by(id = item.actor_id).one_or_none()
            actor_list.append(actor_data)
          movie["pariticipatedActors"] = [Actors.format(item) for item in actor_list]
          actor_list = []
            
    except:
        print(sys.exc_info())
        abort(404)
    return jsonify({"success": True, "movieList": movie_list})
  
  @app.route('/movies', methods=['POST'])
  @requires_auth(permission = "create:movies")
  def create_movie_handler(payload):
    movie_list = Movies.query.all()
    film_list = Films.query.all()
    movie_id_list = [item.id for item in movie_list]
    film_id_list = set([item.id for item in film_list])
    max_movie_id = Movies.query.order_by(db.desc(Movies.id)).first()
    max_film_id = Films.query.order_by(db.desc(Films.id)).first()
    new_id = 1
    film_id = 1
    if max_movie_id != None:
      new_id = find_missing_id(total_records= max_movie_id.id, id_list = movie_id_list)
      
    if max_film_id != None:
      film_id = find_missing_id(total_records= max_film_id.id, id_list = film_id_list)
    try:
        movie_info_client = json.loads(request.data)
        Movies(id= new_id,title= movie_info_client['title'], release_date=movie_info_client['releaseDate']).insert()
        movie_list = Movies.query.order_by(db.desc(Movies.id)).all()
        movie_list = [Movies.format(item) for item in movie_list]
        participated_actor_list = movie_info_client['pariticipatedActors']
        for actor in participated_actor_list:
          Films(id=film_id,actor_id=actor['id'], movie_id=new_id).insert()
        print(movie_list)
    except:
        print(sys.exc_info())
        abort(422)
    return jsonify({"success": True, "movieList": movie_list})
  
  @app.route('/movies-update-info', methods=['PATCH'])
  @requires_auth(permission = "update:movies")
  def update_movie_handler(payload):
    updated_movie = {}
    film_list = Films.query.all()
    film_id_list = set([item.id for item in film_list])
    max_film_id = Films.query.order_by(db.desc(Films.id)).first()
    film_id = 1
    if max_film_id != None:
      film_id = find_missing_id(total_records= max_film_id.id, id_list = film_id_list)
    try:
        search_id = request.args.get('movie_id', 1, int)
        update_info = json.loads(request.data)
        searched_movie = Movies.query.filter_by(id = search_id).one_or_none()
        searched_movie.title = update_info['title']
        searched_movie.release_date = update_info['releaseDate']
        Movies(id= search_id,title= searched_movie.title, release_date=searched_movie.release_date).update()
        film_db_data = db.session.query(Films).filter_by(movie_id = search_id).all()
        film_db_data_id = [item.actor_id for item in film_db_data]
        if len(film_db_data) != 0 and len(update_info['pariticipatedActors']) != 0:
          film_id = film_db_data[0].id
          for actor in update_info['pariticipatedActors']:
            actor_db_data = db.session.query(Films).filter_by(actor_id = actor['id'], movie_id = search_id).one_or_none()
              
            if actor_db_data != None and actor['id'] not in film_db_data_id:
              db.session.query(Films).filter_by(actor_id = actor['id']).delete()
              db.session.commit()

            if actor_db_data == None:
              Films(id = film_id, actor_id= actor['id'], movie_id= search_id).insert()

        if len(film_db_data) == 0 and len(update_info['pariticipatedActors']) != 0:
          for actor in update_info['pariticipatedActors']:
            Films(id = film_id, actor_id= actor['id'], movie_id= search_id).insert()
            
        if len(update_info['pariticipatedActors']) == 0:
          db.session.query(Films).filter_by(movie_id = search_id).delete()
          db.session.commit()

        updated_movie = update_info
        updated_movie['id'] = search_id
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(422)
    finally:
        db.session.close()
    return jsonify({"success": True, "updatedMovie": updated_movie})
  
  @app.route('/movies-eviction', methods=['DELETE'])
  @requires_auth(permission = "delete:movies")
  def remove_movie_handler(payload):
    is_removed = False
    try:
        search_id = request.args.get('movie_id', 1, int)
        searched_movie = Movies.query.filter_by(id = search_id).one_or_none()
        if searched_movie == None:
          abort(404)
        db.session.query(Films).filter_by(movie_id = search_id).delete()
        db.session.commit()
        searched_movie.delete()
        # movie_list = Movies.query.order_by(db.asc(Movies.id)).all()
        # for index, movie  in enumerate(movie_list):
        #   movie.id = index + 1
        #   Movies(id= movie.id,title= movie.title, release_date= movie.release_date).update()
        is_removed = True
    except:
        db.session.rollback()
        print(sys.exc_info())
        abort(422)
    finally:
        db.session.close()
    return jsonify({"success": True, "isRemoved": is_removed })
  
  @app.route('/actors-all', methods = ['GET'])
  @requires_auth(permission = "get:actors")
  def get_all_actor_handler(payload):
    actor_list = []
    try:
      actor_list = Actors.query.all()
      actor_list = [Actors.format(item) for item in actor_list]
    except:
      print(sys.exc_info())
      abort(422)
    return jsonify({"success": True, "actorList": actor_list})
  
  @app.route('/casted-actors', methods = ['GET'])
  @requires_auth(permission = "get:actors")
  def get_casted_actor_handler(payload):
    actor_list = []
    try:
      movie_id = request.args.get('movieId', -1, int)
      casted_actor_id_list = Films.query.filter_by(movie_id = movie_id).all()
      for item in casted_actor_id_list:
        actor_data = Actors.query.filter_by(id = item.actor_id).one_or_none()
        actor_list.append(actor_data)
      actor_list = [Actors.format(item) for item in actor_list]
    except:
      print(sys.exc_info())
      abort(422)
    return jsonify({"success": True, "actorList": actor_list})
  
  @app.route('/actors-filter', methods = ['POST'])
  @requires_auth(permission = "get:actors")
  def search_actor_handler(payload):
    actor_list = []
    try:
      actor_search_info = json.loads(request.data)
      actor_name = actor_search_info["name"]
      actor_gender = actor_search_info["gender"]
      actor_age = actor_search_info["age"]
      print(actor_search_info)
      actor_list = Actors.query.filter(Actors.name.ilike(f'%{actor_name}%') & (Actors.gender == actor_gender) & (Actors.age == str(actor_age))).all()
      actor_list = [Actors.format(item) for item in actor_list]
    except:
      print(sys.exc_info())
      abort(422)
    return jsonify({"success": True, "actorList": actor_list})
  
  @app.route('/actors', methods = ['POST'])
  @requires_auth(permission = "create:actors")
  def create_actor_handler(payload):
    actor_list = Actors.query.all()
    actor_id_list = [item.id for item in actor_list]
    max_id = Actors.query.order_by(db.desc(Actors.id)).first()
    new_id = 1
    if max_id != None:
      new_id = find_missing_id(total_records= max_id.id, id_list = actor_id_list)
    try:
      actor_data = json.loads(request.data)
      Actors(id=new_id, name=actor_data['name'], age=actor_data['age'], gender=actor_data['gender']).insert()
      actor_list = Actors.query.order_by(db.desc(Actors.id)).all()
      actor_list = [Actors.format(item) for item in actor_list]
    except:
        print(sys.exc_info())
        abort(422)
    return jsonify({"success": True, "actorList": actor_list})
  
  @app.route('/actors-update-info', methods=['PATCH'])
  @requires_auth(permission = "update:actors")
  def update_actor_handler(payload):
    updated_actor = {}
    try:
        actor_id = request.args.get('actor_id', 1, int)
        update_info = json.loads(request.data)
        searched_actor = Actors.query.filter_by(id = actor_id).one_or_none()
        searched_actor.name = update_info['name']
        searched_actor.age = update_info['age']
        searched_actor.gender = update_info['gender']
        Actors(id=searched_actor.id, name=searched_actor.name,age=searched_actor.age, 
               gender=searched_actor.gender).update()
        updated_actor = update_info
        updated_actor['id'] = actor_id
    except:
        print(sys.exc_info())
        abort(422)
    return jsonify({"success": True, "updatedActor": updated_actor})
  
  @app.route('/actors-eviction', methods=['DELETE'])
  @requires_auth(permission = "delete:actors")
  def remove_actor_handler(payload):
    try:
        actor_id = request.args.get('actor_id', -1, int)
        db.session.query(Films).filter_by(actor_id = actor_id).delete()
        db.session.commit()
        searched_actor = Actors.query.filter_by(id = actor_id).one_or_none()
        searched_actor.delete()
        actor_list = Actors.query.order_by(db.asc(Actors.id)).all()
        actor_list = Actors.query.all()
        actor_list = [Actors.format(item) for item in actor_list]
        print(actor_list)
    except:
      print(sys.exc_info())
      abort(422)
    return jsonify({"success": True, "actorList": actor_list})

  '''
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return (jsonify({"success": False, "error": 404, "message": "resource not found"}),404,)
  
  @app.errorhandler(400)
  def bad_request(error):
    return (jsonify({"success": False, "error": 400, "message": "bad request"}), 400)
  
  @app.errorhandler(422)
  def unprocessable(error):
    return (jsonify({"success": False, "error": 422, "message": "unprocessable"}),422)
  
  @app.errorhandler(405)
  def not_allowed(error):
    return (jsonify({"success": False, "error": 405, "message": "method not allowed"}), 405)
  
  return app
APP = create_app()
db = SQLAlchemy(APP)
migrate = Migrate(APP, db)
if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)