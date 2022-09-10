import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors

authenMovieToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVpcEJ2N0NFV3pDTGpvMmJxd0xGQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hNWVlaDRjcS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxMDc1YTAyZWM1MWMxZTlkYzU2NWM3IiwiYXVkIjoiQ2FwU3RvbmUtYXBwIiwiaWF0IjoxNjYyNzk1OTUyLCJleHAiOjE2NjI4MDMxNTIsImF6cCI6Im03bkRqa29qTmpDMHp1bUJBR1pHOXRrQkJMWHdPWDVGIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.SvkN8ic2w3cgN4Z_E43oAwO2qVCtXC53307rx5AXEI-YE_yfaZEssrxCWpaOYmPF7yC3oHT5tGvtuTaOPInsr-xEuBQ3tM0B4nrUhBMAzfII9RwpUOLfoS0Hm3N40RT2QaLf5OOwVdMN7iSmHRl5iZfVxcgu2OQSwByI3BYkOhYHoMsJFGWk3j72UsV8C9k0lSj0Z8XPfOnZDuGWCnxj232vDzbXmfELGTBXyr8Bdf_dOEzdVkxALn8S0UiJKVFyAzSeVc4EaHmuPCpo_i_0yIeFvHtjNOap94Kx2tn7x7kCW6uhhyB2qa2DWThhxzMkZrcFVFJePjtXq1fN_fzTWw"

class TriviaTestCase(unittest.TestCase):
 """This class represents the capstone test case"""
 def setUp(self):
  """Define test variables and initialize app."""
  self.app = create_app()
  self.client = self.app.test_client
  self.headers = {"Authorization": "{} {}".format("Bearer", authenMovieToken)}
  self.database_name = "TODO"
  # self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '123', 'localhost:5432', self.database_name)
  # setup_db(self.app, self.database_path)
  self.database_path = "postgresql+psycopg2://cmsrraognpmaqi:413c93c2cabff045b2bb6910aa152d4f611d582cffa2f1652701518a8d4f1189@ec2-107-23-76-12.compute-1.amazonaws.com:5432/dehkajpu6edohp?sslmode=require"
  self.mock_movie_data = {
    "id": 1,
    "releaseDate": "",
    "title": "test1",
    "pariticipatedActors": [
        {
            "id": 8,
            "name": "test actor name 1",
            "age": "25",
            "gender": "Male"
        },
        {
            "id": 9,
            "name": "test actor name 2",
            "age": "25",
            "gender": "Male"
        }
    ]
  }
  # binds the app to the current context
  with self.app.app_context():
   self.db = SQLAlchemy()
   self.db.init_app(self.app)
   self.db.create_all()
   
 def tearDown(self):
  """Executed after reach test"""
  pass
 
 #test get movie success when application starts
 def test_get_movie_handler_success(self):
  res = self.client().get('/movies?movieName=space force', headers = self.headers)
  data = json.loads(res.data)
  # print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["movieList"]), 0)

 #test get movie fail when application starts
 def test_404_failed_get_movie_handler_success(self):
  res = self.client().get('/movies?movieName=movie name is not existed', headers = self.headers)
  data = json.loads(res.data)
  # print(data)
  self.assertEqual(res.status_code, 404)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "resource not found")

 #test create movie success when application starts
 def test_create_movie_handler_success(self):
  res = self.client().post('/movies', json = self.mock_movie_data, headers = self.headers)
  data = json.loads(res.data)
  # print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["movieList"]), 0)
  
 #test create movie fail when application starts
 def test_422_failed_create_movie_handler(self):
  error_movie_data = self.mock_movie_data.pop('pariticipatedActors')
  res = self.client().post('/movies', json = error_movie_data, headers = self.headers)
  data = json.loads(res.data)
  # print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")
  
 #test update movie success when application starts
 def test_update_movie_handler_success(self):
  movie_update_info = self.mock_movie_data
  movie_update_info['title'] = movie_update_info['title'] + 'updated info' + str(movie_update_info['id'])
  # print(movie_update_info)
  res = self.client().patch('/movies-update-info?movie_id=1', json = movie_update_info, headers = self.headers)
  data = json.loads(res.data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["updatedMovie"]), 0)
  
 #test update movie fail when application starts
 def test_404_failed_update_movie_handler(self):
  movie_update_info = self.mock_movie_data
  movie_update_info['title'] = movie_update_info['title'] + 'updated info' + str(movie_update_info['id'])
  res = self.client().patch('/movies-update-info?movie_id=100', json = movie_update_info, headers = self.headers)
  data = json.loads(res.data)
  # print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")

 #test remove movie success when application starts
 def test_remove_movie_handler_success(self):
  res = self.client().delete('/movies-eviction?movie_id=1', headers = self.headers)
  data = json.loads(res.data)
  # print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertEqual(data["isRemoved"], True)

 #test remove movie fail when application starts
 def test_422_failed_remove_movie_handler(self):
  res = self.client().delete('/movies-eviction?movie_id=2022', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
 unittest.main()
