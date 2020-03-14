# CheatSheet Application
Udacity Full Stack Nanodegree Capstone Project

## Acknowledgements
- Udacity has provided a substantial amount of the learning that made this application possible
- Error pages have been forked from https://codepen.io/hellochad/pen/weMpgE
- Would not have been possible without the help and support of an exceptional software development community
  
## Purpose
This is a cheat-sheet application developed to give classroom teachers the ability to create interactive web-based cheat sheet(s) for his/her students for any categories that they see fit. The basic workflow is that a teacher upon being setup in Auth0 is able to create new Categories for cheat sheets. Each of those Categories then can be turned into its own cheat sheet. The cheat sheet consists of a bunch of Concepts that the teacher wants the students to be able to see grouped together into Topics. 

## Current Functionality
- Frontend allows all users to view Categories (homepage) and Cheatsheets
- API allows users to interact with database
- If a concept has a URL tied to it, clicking on the rocket-ship icon next to the concept will launch the URL in a new tab
  - This is to allow expansion upon topics by linking to websites with further information (documentation, wikipedia, etc.)
- Topics have a max-height so once they get to a certain size, users can scroll to see hidden content

### Teachers
- Create, Edit, and Delete Categories, Topics, and Concepts using API endpoints

### Students
- View Categories home page (shows all Categories)
- View Cheatsheets

## Future Functionality
- Users (students & teachers) can post comments about particular concepts, topics, and/or categories to create a conversation thread related to each
- Teachers can perform CRUD functionality directly from front-end
- Teachers could group Categories by Course
- Teachers & Students can upvote a concept. Most upvoted concepts are at the top of Topics and most upvoted Topics are at the top of cheatsheet.
- Teachers can toggle an "Edit" or "Developer" mode which toggles the CRUD icons on or off

## Dependencies
- All required dependencies can be found in requirements.txt

## Local Dev
- Steps to run locally
1) Fork repo: https://github.com/JaySoftwareSolutionsLLC/Udacity-FSND-Capstone
2) navigate to folder
3) run pip install -r requirements.txt
4) run export DATABASE_URL=sqlite:///app.db
5) run python app.py

```Bash
cd <folder_name>
pip install -r requirements.txt
export DATABASE_URL=sqlite:///app.db
python app.py
```

## Hosting
App is hosted on Heroku and can be found at: https://flask-test-4.herokuapp.com/

## Authorization
Application uses Auth0 to provide 3rd party authentication
Steps to receive an access token:
1) Navigate to https://bjb.auth0.com/authorize?audience=cheatsheet&response_type=token&client_id=tJQnGJ8VZ8s1QqbhcvE5bbHJ94HQQvEO&redirect_uri=https://flask-test-4.herokuapp.com/categories
2) Login with one of these two accounts:
   1) student@gmail.com | Student1234
   2) teacher@gmail.com | Teacher1234

## API

### Roles

#### Teacher
Represents a teacher for a given course. They have the ability to create new cheatsheets (Category model) as well as full create, update, edit, and delete capabilities on all content pertinent to those cheatsheets (Topic & Concept models)

#### Student
Represents a student of a given course. They are only able to view (read) cheatsheets but cannot create, edit, or delete content in any way

### Endpoints

#### Category endpoints
Category endpoints allow Teachers to perform CRUD maintenance on Categories


##### GET ALL CATEGORIES
endpoint: /api/categories
method: GET
permissions: No permissions required
response: 
```JSON
{
    "categories": [
        {
            "description": "Flask application development cheat sheet",
            "id": 1,
            "name": "Flask",
            "topics": [
                {
                    "category_id": 1,
                    "concepts": [],
                    "description": "Python Flask Programming Best Practices",
                    "id": 1,
                    "name": "Best Practices"
                },
                {
                    "category_id": 1,
                    "concepts": [
                        {
                            "description": "Export a DATABASE_URL variable locally which can then be retrieved by importing os. This will connect application to <name.db>",
                            "id": 1,
                            "name": "export DATABASE_URL=sqlite:///<name.db>",
                            "topic_id": 2,
                            "url": "https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/"
                        },
                        {
                            "description": "Export a DATABASE_URL variable locally which can then be retrieved by importing os. This will connect application to <data_base_name>",
                            "id": 2,
                            "name": "export DATABASE_URL=postgres://<u>:<p>@localhost:<p>/<db>",
                            "topic_id": 2,
                            "url": null
                        }
                    ],
                    "description": "How to connect to databases inside of using Python Flask",
                    "id": 2,
                    "name": "Database Conn."
                },
                {
                    "category_id": 1,
                    "concepts": [],
                    "description": "Establishing endpoints inside of a Flask Application",
                    "id": 3,
                    "name": "Routing"
                }
            ]
        },
        {
            "description": "Python development cheat sheet",
            "id": 2,
            "name": "Python",
            "topics": []
        },
        {
            "description": "Cheat sheet for Udacity specific content",
            "id": 3,
            "name": "Udacity",
            "topics": []
        }
    ],
    "success": true,
    "total_categories": 4
}
```

##### CREATE CATEGORY
endpoint: /api/categories
method: POST
permissions: "create:any"
request:
```JSON
{
	"name" : "test-name",
	"description" : "test-desc"
}
```
response: 
```JSON
{
    "request": {
        "description": "test-desc",
        "id": 5,
        "name": "test-name-2",
        "topics": []
    },
    "success": true
}
```

##### UPDATE CATEGORY
endpoint: /api/categories/<int:category_id>/update
method: PATCH
permissions: "update:any"
request:
```JSON
{
	"name" : "Udacity-TEST",
	"description" : "Cheat sheet for Udacity specific content"
}
```
response: 
```JSON
{
    "category": {
        "description": "Cheat sheet for Udacity specific content",
        "id": 5,
        "name": "Udacity-TEST",
        "topics": []
    },
    "success": true
}
```

##### DELETE CATEGORY
endpoint: /api/categories/<int:category_id>
method: DELETE
permissions: "delete:any"
response: 
```JSON
{
    "request": {
        "description": "Cheat sheet for Udacity specific content",
        "id": 5,
        "name": "Udacity-TEST",
        "topics": []
    },
    "success": true
}
```

##### GET SINGLE CATEGORY
endpoint: /api/categories/<int:category_id>
method: GET
permissions: No permissions required
response: 
```JSON
{
    "category": {
        "description": "Flask application development cheat sheet",
        "id": 1,
        "name": "Flask",
        "topics": [
            {
                "category_id": 1,
                "concepts": [],
                "description": "Python Flask Programming Best Practices",
                "id": 1,
                "name": "Best Practices"
            },
            {
                "category_id": 1,
                "concepts": [
                    {
                        "description": "Export a DATABASE_URL variable locally which can then be retrieved by importing os. This will connect application to <name.db>",
                        "id": 1,
                        "name": "export DATABASE_URL=sqlite:///<name.db>",
                        "topic_id": 2,
                        "url": "https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/"
                    },
                    {
                        "description": "Export a DATABASE_URL variable locally which can then be retrieved by importing os. This will connect application to <data_base_name>",
                        "id": 2,
                        "name": "export DATABASE_URL=postgres://<u>:<p>@localhost:<p>/<db>",
                        "topic_id": 2,
                        "url": null
                    }
                ],
                "description": "How to connect to databases inside of using Python Flask",
                "id": 2,
                "name": "Database Conn."
            },
            {
                "category_id": 1,
                "concepts": [],
                "description": "Establishing endpoints inside of a Flask Application",
                "id": 3,
                "name": "Routing"
            }
        ]
    },
    "success": true
}
```

#### Topic Endpoints

##### CREATE TOPIC
endpoint: /api/topics
method: POST
permissions: "create:any"
request:
```JSON
{
	"name" : "test-topic",
	"description" : "test-topic-desc",
	"category_id": 1
}
```
response: 
```JSON
{
    "new_topic": {
        "category_id": 1,
        "concepts": [],
        "description": "test-topic-desc",
        "id": 4,
        "name": "test-topic"
    },
    "request": {
        "category_id": 1,
        "description": "test-topic-desc",
        "name": "test-topic"
    },
    "success": true
}
```

##### UPDATE TOPIC
endpoint: /api/topics/<int:topic_id>/update
method: PATCH
permissions: "update:any"
request:
```JSON
{
	"name" : "test-topic-E",
	"description" : "test-topic-desc"
}
```
response: 
```JSON
{
    "success": true,
    "topic": {
        "category_id": 1,
        "concepts": [],
        "description": "test-topic-desc",
        "id": 4,
        "name": "test-topic-E"
    }
}
```

##### DELETE TOPIC
endpoint: /api/topics/<int:topic_id>
method: DELETE
permissions: "delete:any"
response: 
```JSON
{
    "request": {
        "category_id": 1,
        "concepts": [],
        "description": "test-topic-desc",
        "id": 4,
        "name": "test-topic-E"
    },
    "success": true
}
```

#### Concept Endpoints

##### CREATE CONCEPT
endpoint: /api/concepts
method: POST
permissions: "create:any"
request:
```JSON
{
	"name" : "test-concept",
	"description" : "test-concept-desc",
	"topic_id": 1,
	"url": "https://testurl.com"
}
```
response: 
```JSON
{
    "new_concept": {
        "description": "test-concept-desc",
        "id": 3,
        "name": "test-concept",
        "topic_id": 1,
        "url": "https://testurl.com"
    },
    "request": {
        "description": "test-concept-desc",
        "name": "test-concept",
        "topic_id": 1,
        "url": "https://testurl.com"
    },
    "success": true
}
```

##### UPDATE CONCEPT
endpoint: /api/concepts/<int:concept_id>/update
method: PATCH
permissions: "update:any"
request:
```JSON
{
	"name" : "test-concept-E",
	"description" : "test-concept-desc",
	"url": "https://testurl.com"
}
```
response: 
```JSON
{
    "concept": {
        "description": "test-concept-desc",
        "id": 3,
        "name": "test-concept-E",
        "topic_id": 1,
        "url": "https://testurl.com"
    },
    "success": true
}
```

##### DELETE CONCEPT
endpoint: /api/concepts/<int:concept_id>
method: DELETE
permissions: "delete:any"
response: 
```JSON
{
    "request": {
        "description": "test-concept-desc",
        "id": 3,
        "name": "test-concept-E",
        "topic_id": 1,
        "url": "https://testurl.com"
    },
    "success": true
}
```

### JWTs
Teacher JWT: (will expire Mar 15th 2020 @ 2:33pm EST)
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2ZDIyZGExMDg4NWIwY2E2YTg1NjllIiwiYXVkIjoiY2hlYXRzaGVldCIsImlhdCI6MTU4NDIxMDc5MiwiZXhwIjoxNTg0Mjk3MTkyLCJhenAiOiJ0SlFuR0o4Vlo4czFRcWJoY3ZFNWJiSEo5NEhRUXZFTyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.KDtic9q5Nr07pxnIDnRcFz6qizZYZeUQwHT91EAMiUlUvaT7sW0hDZZp4ZS_55csYlDpADKDMJ1Kt0AkKnyz7bX6-Ttc-91OdGTGKF3ARpXuaQOCxiqJaM_zqmiTkdNB4dxaCS2FBXdY6RToxChcNaxd4vcz3CZHoWRr5THSMkRffjS1k23Y9p2q4X09y3zrXE64-o9T_BJs7vqyerDGfv06qq6_7iJLRVGTzFHqB8odN0E0EaaHXs91fNAbAncy11FS8ccreIc3XVLzqdL8DHT5HNJ1Tcfd1MBSFLWob6QilszOcYuMBMS7-oLk8h2HrGwRIWBrGhM4Q-whsSokGA

Student JWT: (will expire Mar 15th 2020 @ 2:39pm EST)
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2ZDIyOTAwODQ1NzEwYzkyMjE0OGUzIiwiYXVkIjoiY2hlYXRzaGVldCIsImlhdCI6MTU4NDIxMTE0NSwiZXhwIjoxNTg0Mjk3NTQ1LCJhenAiOiJ0SlFuR0o4Vlo4czFRcWJoY3ZFNWJiSEo5NEhRUXZFTyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.JJDIBm5x9KiZxCOpp4HDYl5Rcduz3XgxTBLEyyNfMUuZlUfrx-HiH6gEoAlC5RHDlIdcJJad5whL1sgePJ43RZZRZS5gHruxAGl-mw1x4rbWQG3P16yRpX9zIHOJ0IRE98zsXxoNL1NdCthkh22RhCFHkquSxwPMBtRGKriGQHLFEWKFUWjlSoZeQW0gnjR33R7hTfkqejVhIYCJ7u1szB2gJL7E3KVmFtdUHdOoPLWpPbGgkyuWpN7uoJ3Wg1iOK4HyGGBFzUKqTPU3spo0BM9k0rmyQn_8hDDrq5Dd1LFQuzP6gzq4WvHcgwca87S9iT-oGnfq2dC3rXBbfZpFnA
