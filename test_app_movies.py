import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors

authenMovieToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVpcEJ2N0NFV3pDTGpvMmJxd0xGQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hNWVlaDRjcS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxMDc2YzBiZGVhODBmYzY1ZWE4OGEwIiwiYXVkIjoiQ2FwU3RvbmUtYXBwIiwiaWF0IjoxNjYyMTI4MzQ5LCJleHAiOjE2NjIxMzU1NDksImF6cCI6Im03bkRqa29qTmpDMHp1bUJBR1pHOXRrQkJMWHdPWDVGIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiY3JlYXRlOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyJdfQ.YE-OLt2p0bH9ZOz3lVp7uGneEz4mV-aRVH0SCMj745vb4aS7O-qL4ZDQFWE3B6Zn2WjpVkaOP1alEbe_wAp4aQFpjAajM76j_vDBgT2Nt3E9lFMmpUcaLG9JhiCGeoaXVzMgrJZvsfoHio7VLAlAxdBM7-LpdTr06kKtAFPg_hf2nk2G7n3M940MAMAGRGjpFexuuttQYZhr3LCYvF_Mgu4ygOeDX4LsKA1BDs0pGzN_MXNFzKEo7SoxB2CbjeKquahWZUUmbbWVX2drKMPKvVr4kI-xa_3YtC48Z2zuWhPnU9KYrpu6vNr3VPY9HqGoQVZRPbqCGKAs3jnTTLTWLA"

class TriviaTestCase(unittest.TestCase):
 """This class represents the capstone test case"""
 def setUp(self):
  """Define test variables and initialize app."""
  self.app = create_app()
  self.client = self.app.test_client
  self.headers = {"Authorization": "{} {}".format("Bearer", authenMovieToken)}
  self.database_name = "TODO"
  self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '123', 'localhost:5432', self.database_name)
  setup_db(self.app, self.database_path)
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
