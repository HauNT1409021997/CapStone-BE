from email import header
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors

authenActorToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlVpcEJ2N0NFV3pDTGpvMmJxd0xGQiJ9.eyJpc3MiOiJodHRwczovL2Rldi1hNWVlaDRjcS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjMxMDc2YzBiZGVhODBmYzY1ZWE4OGEwIiwiYXVkIjoiQ2FwU3RvbmUtYXBwIiwiaWF0IjoxNjYyMTI4MzQ5LCJleHAiOjE2NjIxMzU1NDksImF6cCI6Im03bkRqa29qTmpDMHp1bUJBR1pHOXRrQkJMWHdPWDVGIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6YWN0b3JzIiwiY3JlYXRlOm1vdmllcyIsImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyJdfQ.YE-OLt2p0bH9ZOz3lVp7uGneEz4mV-aRVH0SCMj745vb4aS7O-qL4ZDQFWE3B6Zn2WjpVkaOP1alEbe_wAp4aQFpjAajM76j_vDBgT2Nt3E9lFMmpUcaLG9JhiCGeoaXVzMgrJZvsfoHio7VLAlAxdBM7-LpdTr06kKtAFPg_hf2nk2G7n3M940MAMAGRGjpFexuuttQYZhr3LCYvF_Mgu4ygOeDX4LsKA1BDs0pGzN_MXNFzKEo7SoxB2CbjeKquahWZUUmbbWVX2drKMPKvVr4kI-xa_3YtC48Z2zuWhPnU9KYrpu6vNr3VPY9HqGoQVZRPbqCGKAs3jnTTLTWLA"

class TriviaTestCase(unittest.TestCase):
 """This class represents the capstone test case"""
 def setUp(self):
  """Define test variables and initialize app."""
  self.app = create_app()
  self.client = self.app.test_client
  self.headers = {"Authorization": "{} {}".format("Bearer", authenActorToken)}
  self.database_name = "TODO"
  self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '123', 'localhost:5432', self.database_name)
  setup_db(self.app, self.database_path)
  self.mock_actor_search_data = {
    "name": "Lilly",
    "gender": "Female",
    "age": 25
		}
  
  self.mock_actor_create_data = {
    "id": 1,
    "name": "test actor name 2",
    "age": "25",
    "gender": "Male"
		}
  
  self.mock_actor_update_data = {
    "id": 10,
    "name": "test actor name updated",
    "age": "25",
    "gender": "Male"
		}
  # binds the app to the current context
  with self.app.app_context():
   self.db = SQLAlchemy()
   self.db.init_app(self.app)
   self.db.create_all()
   
 def tearDown(self):
  """Executed after reach test"""
  pass
 
 #test get all actor success when application starts
 def test_get_all_actor_handler_success(self):
  res = self.client().get('/actors-all', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["actorList"]), 0)
  
 #test get all actor fail when application starts
 def test_422_failed_get_all_actor_handler(self):
  res = self.client().get('/actors-all', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")

 #test get casted actor success when application starts
 def test_get_casted_actor_handler_success(self):
  res = self.client().get('/casted-actors?movieId=1', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["actorList"]), 0)
 
 #test get casted actor fail when application starts
 def test_422_failed_get_casted_actor_handler(self):
  res = self.client().get('/casted-actors?movieId=', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")
 
 #test search actor success when application starts
 def test_search_actor_handler_success(self):
  res = self.client().post('/actors-filter', json =self.mock_actor_search_data, headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["actorList"]), 0)
 
 #test search actor fail when application starts
 def test_422_failed_search_actor_handler(self):
  error_search_data = self.mock_actor_search_data.pop('age')
  res = self.client().post('/actors-filter', json = error_search_data, headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")
 
 #test create actor success when application starts
 def test_create_actor_handler_success(self):
  res = self.client().post('/actors', json =self.mock_actor_create_data, headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["actorList"]), 0)
 
 #test create actor fail when application starts
 def test_422_failed_create_actor_handler(self):
  res = self.client().post('/actors-filter', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")
 
 #test update actor success when application starts
 def test_update_actor_handler_success(self):
  res = self.client().patch('/actors-update-info', json =self.mock_actor_update_data, headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["updatedActor"]), 0)
 
 #test update actor fail when application starts
 def test_422_failed_update_actor_handler(self):
  res = self.client().patch('/actors-update-info', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")
 
 #test remove actor success when application starts
 def test_remove_actor_handler_success(self):
  res = self.client().delete('/actors-eviction?actor_id=10', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 200)
  self.assertEqual(data["success"], True)
  self.assertGreaterEqual(len(data["actorList"]), 0)
 
 #test remove actor fail when application starts
 def test_422_failed_remove_actor_handler(self):
  res = self.client().delete('/actors-eviction', headers = self.headers)
  data = json.loads(res.data)
  print(data)
  self.assertEqual(res.status_code, 422)
  self.assertEqual(data["success"], False)
  self.assertEqual(data["message"], "unprocessable")

# Make the tests conveniently executable
if __name__ == "__main__":
 unittest.main()
