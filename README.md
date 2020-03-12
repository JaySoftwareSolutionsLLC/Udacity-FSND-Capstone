# Udacity-FSND-Capstone
Udacity Full Stack Nanodegree Capstone Project
URL - https://flask-test-4.herokuapp.com/

## Project Overview

### Purpose

### Dependencies, Local Dev, and Hosting

### API

### RBAC Controls

## Authorization
Application uses Auth0 to provide 3rd party authentication

### Roles

#### Teacher
Represents a teacher for a given course. They have the ability to create new cheatsheets (Category model) as well as full create, update, edit, and delete capabilities on all content pertinent to those cheatsheets (Topic & Concept models)

#### Student
Represents a student of a given course. They are only able to view (read) cheatsheets but cannot create, edit, or delete content in any way

Teacher JWT = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIwNzY1MTYxMjg2ODU5MTEwNDQiLCJhdWQiOlsiY2hlYXRzaGVldCIsImh0dHBzOi8vYmpiLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODM5NjUxMTUsImV4cCI6MTU4Mzk3MjMxNSwiYXpwIjoidEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.qxx27bvY5SFrHWrsjVTuOKyYTnvqWZU9dLa8EGcHqX_Qgk6u5Mi4TfWmjoWx1VFEyuuvJ1EkArAqe_6LymIkrAjsouBVuqym1N6_MrG7O4JrgILKqj6rkIhPXpAXluhYBgd3isbWKtOHDaoycYEqaV-018h0AvohNnSmBjgXlwhaPTIjg-8icORomE4Te0weyYHjmUW2Xa_PWSF_SvfgmHVmVosuHGeBBfhVCgv7gIX3byW6ae2P4iESfxs44omm_wXsTpaQMOVUt3iiUNR3BWH1oDqg-Rpzx20xCXJE6BpWHRzhW1fLIqRv-cQnoXzLbhhw5I2tLxDPErAMZPJSNg

Student JWT =


General Notes:
Need to run "export EXCITED=true" or "export EXCITED=false" AND "export DATABASE_URL=sqlite:///app.db" OR "postgres://postgres:$u944jAk161519@localhost:5432/udacity_fsnd_capstone" before running app locally
Enhancement idea: Edit mode available to teachers only. Toggles whether CRUD functionality is possible.
May need to update requirements file for auth.py to work on production server