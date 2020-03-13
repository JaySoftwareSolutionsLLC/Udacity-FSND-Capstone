# CheatSheet Application
Udacity Full Stack Nanodegree Capstone Project

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

## API

### Roles

#### Teacher
Represents a teacher for a given course. They have the ability to create new cheatsheets (Category model) as well as full create, update, edit, and delete capabilities on all content pertinent to those cheatsheets (Topic & Concept models)

#### Student
Represents a student of a given course. They are only able to view (read) cheatsheets but cannot create, edit, or delete content in any way

### Endpoints

### JWTs
Teacher JWT: (will expire April 12th 2020 @ 4:52pm EST)
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIwNzY1MTYxMjg2ODU5MTEwNDQiLCJhdWQiOlsiY2hlYXRzaGVldCIsImh0dHBzOi8vYmpiLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODQxMzI4MTIsImV4cCI6MTU4NDIxOTIxMCwiYXpwIjoidEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.eKRjc4mw36kDys9kqf_1-5q52LWRUHb0CxtX4QNqGzNOxusct5r3KcO4UKKYD9AVT284RQHtbo2k-nbF4pk9xJKlcU8dosJDiVZJ3ZYC7dQzbvMbRnsbBcFuV9HhvHFcwOzzWh9wPu_ZXHRi0UvusMOSAPACtiCWXjam72uM_y3KOpZqzwHTHCIFbwlKnGSTeGCpv8DiP6wPz_9Yc3SWi4Irr7kEz9WYbGIAKjt4uDg-lQttOxmdaJUr629R4v2R420YsSb5vG7_-16NVXELCafwR6WjlVMBNC1Qoc6ewkYWy6Zj0f0YTn9z3_RURb7dcKLzZpnhxXd5KXMQGyNlTQ

Student JWT: (will expire Mar 14th 2020 @ 4:44pm EST)
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRmOTUxZGEyZDIzZjIwZThhZWU3NTU5IiwiYXVkIjoiY2hlYXRzaGVldCIsImlhdCI6MTU4NDEzMjI0NiwiZXhwIjoxNTg0MjE4NjQ0LCJhenAiOiJ0SlFuR0o4Vlo4czFRcWJoY3ZFNWJiSEo5NEhRUXZFTyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.SWyGwlsdVJPrbQ512AKeetf7icYwbzyUB9THcjxGOM1JmEXBxl9rApPlHILpxh2_AJqDBs2Q8qAsykoMqBaOeyJbi0oYtQC8KQe4JqJxPWZSt67xDlORCTI01IZFUJjRksFB3BJzaS645OnBlDo3moLeR1Mvq-znbrUTD8jdqeb8F-PeLUONypZgEdzZ1n7xLibZBkqoWLJLZaEsY8d7mMnQGY-tKC3Rd3zxup7nkSHY3o0rG0zEGbjh_xgs4EGUTYaij-afVf_7KqVmv-CDKHmi6jdkRjZhPCEOQ1_7oIcmfFNaLDp-ycbMJ8HVdFrTVryLUx2zzP3slJZ3btyjYA
