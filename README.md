



## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, ` https://haunt-capstone-app.herokuapp.com/`, which is set as a proxy in the frontend configuration. 
- Authentication:
	Authen Introduction:
		There are three roles with each role has different permissions.
		In order to use the api of the application. User must login by enter the roles email and the password belows by selecting the login button

	Roles:
		Casting Assistant:
			email: CastingAssitance@gmail.com
			password: CastingAssitance20220901
			permissions: Can view actors and movies

		Casting Director:
			email: CastingDirector@gmail.com
			password: CastingDirector20220901
			permissions: 
				Can view actors and movies
				Add or delete an actor from the database
				Modify actors or movies

		Executive Producer:
			email: ExecutiveProducer@gmail.com
			password: ExecutiveProducer20220901
			permissions: 
				Can view actors and movies
				Add or delete an actor from the database
				Modify actors or movies
				Add or delete a movie from the database

- Api testing:
  api testing introduction:
    A postman file has been setup for three authorized roles to test the api.
    Each file has been named after the role name.
    Before run any testing, please check the following conditions:
      - The brear token must be valid and entered in the file
      - Check the api explanation below to further understand how api purpose and it's parameter meaning
      - Run the app live first to gain a broad view and understandings about the app features

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 405: method not allowed

### Endpoints 
#### GET /movies
- General:
    - Returns a list of movies along with a list of cast participated in the movies.
				- if the api parameter movieName have a value then return a list with only seached results
				- if the value is not found then error message 404 will be invoked
				- the api can be invoked by entering value on the search bar then focus out
- Sample: `curl https://haunt-capstone-app.herokuapp.com/movies?movieName=Water world`

```
request response
{
	"movieList" : [{
      "id": 6,
      "pariticipatedActors": [
        {
          "age": "25",
          "gender": "Male",
          "id": 8,
          "name": "test actor name 1"
        },
        {
          "age": "25",
          "gender": "Male",
          "id": 9,
          "name": "test actor name 2"
        }
      ],
      "releaseDate": "",
      "title": "test1"
    }],
	"success": True
}
```

#### POST /movies
- General:
    - If provided, create movies in the database.
				- If the actor name is selected. Then actor id will be created in table Film in the database.
				- Returns the success value, list of movies. 
- `curl https://haunt-capstone-app.herokuapp.com/movies`
```
request payload
	{
			"id": null,
			"title": "Interstellar",
			"releaseDate": "05092022",
			"pariticipatedActors": [
					{
							"age": "60",
							"gender": "Male",
							"id": 2,
							"name": "Kevin Cosner"
					}
			]
	}

request response

{
	"movieList" : [{
      "id": 6,
      "pariticipatedActors": [
        {
          "age": "25",
          "gender": "Male",
          "id": 8,
          "name": "test actor name 1"
        },
        {
          "age": "25",
          "gender": "Male",
          "id": 9,
          "name": "test actor name 2"
        }
      ],
      "releaseDate": "",
      "title": "test1"
    }],
	"success": True
}
```
#### PATCH /movies-update-info
- General:
				- Update the movie of the given ID if it exists
    - Update the current movie data in table Movies in the database.
				- Update the current film data in table Films in the database.
				- Returns the success value, the newly updated movie. 
- `curl -X PATCH https://haunt-capstone-app.herokuapp.com/movies-update-info?movie_id=1`
```
request payload
movie_id: 1

{
  "id": 1,
  "title": "Interstellar",
  "releaseDate": "05092022",
  "pariticipatedActors": [
    {
      "age": "60",
      "gender": "Male",
      "id": 2,
      "name": "Kevin Cosner"
    },
    {
      "age": "30",
      "gender": "Male",
      "id": 3,
      "name": "Kevin JRK"
    },
    {
      "age": "58",
      "gender": "Male",
      "id": 4,
      "name": "jackie Chan"
    }
  ]
}

request response

{
  "success": true,
  "updatedMovie": {
    "id": 1,
    "pariticipatedActors": [
      {
        "age": "60",
        "gender": "Male",
        "id": 2,
        "name": "Kevin Cosner"
      },
      {
        "age": "30",
        "gender": "Male",
        "id": 3,
        "name": "Kevin JRK"
      },
      {
        "age": "58",
        "gender": "Male",
        "id": 4,
        "name": "jackie Chan"
      }
    ],
    "releaseDate": "05092022",
    "title": "Interstellar"
  }
}

```

#### DELETE /movies-eviction
- General:
    - Deletes the movie of the given ID if it exists. Return the success value.
- `curl -X DELETE https://haunt-capstone-app.herokuapp.com/movies-eviction?movie_id=6`
```
request payload 
movie_id=6

request response
{
  "isRemoved": true,
  "success": true
}
```

#### GET /actors-all
- General:
    - Returns the success value, list of actors. 
- `curl https://haunt-capstone-app.herokuapp.com/actors-all`
```
request response
{
  "actorList": [
    {
      "age": "60",
      "gender": "Male",
      "id": 2,
      "name": "Kevin Cosner"
    },
    {
      "age": "30",
      "gender": "Male",
      "id": 3,
      "name": "Kevin JRK"
    },
    {
      "age": "58",
      "gender": "Male",
      "id": 4,
      "name": "jackie Chan"
    }
  ],
  "success": true
}
```

#### GET /casted-actors
- General:
				- If provided, search movies that matches the movieId property. 
				- Returns the success value, list of actors who were casted into the movie. 
- `curl https://haunt-capstone-app.herokuapp.com/casted-actors?movieId=1`
```
request payload 
movieId: 1

request response
{
  "actorList": [
    {
      "age": "60",
      "gender": "Male",
      "id": 2,
      "name": "Kevin Cosner"
    },
    {
      "age": "30",
      "gender": "Male",
      "id": 3,
      "name": "Kevin JRK"
    },
    {
      "age": "58",
      "gender": "Male",
      "id": 4,
      "name": "jackie Chan"
    },
    {
      "age": "20",
      "gender": "Female",
      "id": 5,
      "name": "Kelly"
    }
  ],
  "success": true
}
```
#### POST /actors-filter
- General:
    - If provided, search actor based on the actor's name, actor's age, actor's gender.
				- Returns the success value, list of actors. 
- `curl https://haunt-capstone-app.herokuapp.com/actors-filter`
```
request payload
{
  "name": "",
  "gender": "Female",
  "age": 25
}

request response
{
  "actorList": [
    {
      "age": "25",
      "gender": "Female",
      "id": 6,
      "name": "Lilly"
    }
  ],
  "success": true
}

```


#### POST /actors
- General:
    - If provided, create actor data in Actors table in the database.
				- Returns the success value, list of actors including newly created actor data. 
- `curl https://haunt-capstone-app.herokuapp.com/actors`
```
request payload
{
  "id": 0,
  "name": "Matt Haddon",
  "age": 10,
  "gender": "Female"
}

request response
{
  "actorList": [
    {
      "age": "15",
      "gender": "Male",
      "id": 12,
      "name": "james"
    },
    {
      "age": "10",
      "gender": "Female",
      "id": 11,
      "name": "Matt Haddon"
    }
  ],
  "success": true
}
```
#### PATCH /actors-update-info
- General:
    - If provided, update the actor's data in the Actors table based on the actor id.
				- Returns the success value, updated actor data. 
- `curl -X PATCH https://haunt-capstone-app.herokuapp.com/actors-update-info?actor_id=12`
```
request payload
{
  "id": 12,
  "name": "james",
  "age": 17,
  "gender": "Male"
}

request response
{
  "success": true,
  "updatedActor": {
    "age": 17,
    "gender": "Male",
    "id": 12,
    "name": "james"
  }
}
```

#### DELETE /actors-eviction
- General:
    - Deletes the actor of the given ID if it exists. Return the success value, list of actors.
				- Deletes the associative data between movie and actor in table Films.
- `curl -X DELETE https://haunt-capstone-app.herokuapp.com/actors-eviction?actor_id=13`
```
request payload 
actor_id: 13

request response
{
  "actorList": [
    {
      "age": "60",
      "gender": "Male",
      "id": 2,
      "name": "Kevin Cosner"
    },
    {
      "age": "30",
      "gender": "Male",
      "id": 3,
      "name": "Kevin JRK"
    },
    {
      "age": "58",
      "gender": "Male",
      "id": 4,
      "name": "jackie Chan"
    },
    {
      "age": "20",
      "gender": "Female",
      "id": 5,
      "name": "Kelly"
    },
    {
      "age": "25",
      "gender": "Female",
      "id": 6,
      "name": "Lilly"
    },
    {
      "age": "35",
      "gender": "Female",
      "id": 7,
      "name": "Gywnet Patrows"
    }
  ],
  "success": true
}
```
