import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify
from app import create_app
from models import setup_db, db, Category, Topic, Concept

from auth.auth import get_token_auth_header

class CheatSheetTestCases(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'sqlite:///test.db'

        # binds the app to the current context
        with self.app.app_context():
            self.db = db
            setup_db(self.app, self.database_path)
            self.db.init_app(self.app)

            # self.db.session.execute(
            #     "TRUNCATE Category RESTART IDENTITY CASCADE")
            # # Create new category for DB
            # cat1 = Category(name='TestCat1', description='This is a test category')
            # self.db.session.add(cat1)
            # self.db.session.commit()

    def tearDown(self):
        """Executed after reach test"""
        pass


    '''
    TESTS
    '''

    def test_always_true(self):
        self.assertTrue(False)

    # Front End Testing

    def test_categories(self):
        res = self.client().get('/categories')
        data = res.data
        # pulling_from_db =  # Need the b to convert 'TestCat1' to binary mode
        # pulling_from_db =  # Need the b to convert 'TestCat1' to binary mode
        self.assertTrue(b'TestCat1' in data)
        self.assertFalse(b'This String For Sure wont exist inside of the returned data...' in data)

    def test_cheatsheet(self):
        res = self.client().get('/categories/1')
        data = res.data
        self.assertTrue(b'TestTop1' in data)
        self.assertTrue(b'TestTop3' in data)
        self.assertTrue(b'TestCon1' in data)
        self.assertFalse(b'This String For Sure wont exist inside of the returned data...' in data)

    # API testing

    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    # Need to tweak these 3 a bit. Running into a timing issue because unit test may run these all at same time and also running into issue with id becoming > 4 after the first delete so may need to refactor to pull id in from response
    def test_create_category(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIwNzY1MTYxMjg2ODU5MTEwNDQiLCJhdWQiOlsiY2hlYXRzaGVldCIsImh0dHBzOi8vYmpiLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODQwNDg3OTAsImV4cCI6MTU4NDA1NTk5MCwiYXpwIjoidEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.VUfCP1-p587bXsv8TfXxQNYxhZDrLmQmk0mVkR9yvFHGKYt2edUg5ViKbJ5qL8Kefljk9C1JQ8yiGR3QorWeFQZjRwG3RKQV1CDOKaWybSpywQQIxrI6ISEYJqv5iCQ9cMBTqiqoBPLlsP85ddR-lVL96a-liu3RcZXgByo5vajbTyAPPxCg36AMxyi3NrlA1ZvGiqdmw9_pelHV4j0_7ai3IG6H3gTP8GjepqlcAAyWcphKkFSYkNs16FXTxGNYy2nVOfmQvJHxwv8H2LHbU3A-Izyty0dvpRCYyMCPUhm9c-oZ-vVAfx2B23AaDB7lHoW1fBIonVrFiiAUG0REug'}
        res = self.client().post('/api/categories', headers=self.headers, json={"name" : "TestCat4", "description" : "This is a test concept for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_edit_category(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIwNzY1MTYxMjg2ODU5MTEwNDQiLCJhdWQiOlsiY2hlYXRzaGVldCIsImh0dHBzOi8vYmpiLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODQwNDg3OTAsImV4cCI6MTU4NDA1NTk5MCwiYXpwIjoidEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.VUfCP1-p587bXsv8TfXxQNYxhZDrLmQmk0mVkR9yvFHGKYt2edUg5ViKbJ5qL8Kefljk9C1JQ8yiGR3QorWeFQZjRwG3RKQV1CDOKaWybSpywQQIxrI6ISEYJqv5iCQ9cMBTqiqoBPLlsP85ddR-lVL96a-liu3RcZXgByo5vajbTyAPPxCg36AMxyi3NrlA1ZvGiqdmw9_pelHV4j0_7ai3IG6H3gTP8GjepqlcAAyWcphKkFSYkNs16FXTxGNYy2nVOfmQvJHxwv8H2LHbU3A-Izyty0dvpRCYyMCPUhm9c-oZ-vVAfx2B23AaDB7lHoW1fBIonVrFiiAUG0REug'}
        res = self.client().patch('/api/categories/4/update', headers=self.headers, json={"name" : "TestCat4-E", "description" : "This is a test concept for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_category(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIwNzY1MTYxMjg2ODU5MTEwNDQiLCJhdWQiOlsiY2hlYXRzaGVldCIsImh0dHBzOi8vYmpiLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODQwNDg3OTAsImV4cCI6MTU4NDA1NTk5MCwiYXpwIjoidEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.VUfCP1-p587bXsv8TfXxQNYxhZDrLmQmk0mVkR9yvFHGKYt2edUg5ViKbJ5qL8Kefljk9C1JQ8yiGR3QorWeFQZjRwG3RKQV1CDOKaWybSpywQQIxrI6ISEYJqv5iCQ9cMBTqiqoBPLlsP85ddR-lVL96a-liu3RcZXgByo5vajbTyAPPxCg36AMxyi3NrlA1ZvGiqdmw9_pelHV4j0_7ai3IG6H3gTP8GjepqlcAAyWcphKkFSYkNs16FXTxGNYy2nVOfmQvJHxwv8H2LHbU3A-Izyty0dvpRCYyMCPUhm9c-oZ-vVAfx2B23AaDB7lHoW1fBIonVrFiiAUG0REug'}
        res = self.client().delete('/api/categories/4', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


    # Error code testing

    ## 401
    def test_unauthorized_user(self):
        res = self.client().post('/api/categories',
                                 json={"name" : "This shouldn't work", "description" : "This shouldn't work"})

        self.assertEqual(res.status_code, 401)

    ## 401 - Expired token
    def test_expired_token(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIwNzY1MTYxMjg2ODU5MTEwNDQiLCJhdWQiOlsiY2hlYXRzaGVldCIsImh0dHBzOi8vYmpiLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODM5NjUxMTUsImV4cCI6MTU4Mzk3MjMxNSwiYXpwIjoidEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.qxx27bvY5SFrHWrsjVTuOKyYTnvqWZU9dLa8EGcHqX_Qgk6u5Mi4TfWmjoWx1VFEyuuvJ1EkArAqe_6LymIkrAjsouBVuqym1N6_MrG7O4JrgILKqj6rkIhPXpAXluhYBgd3isbWKtOHDaoycYEqaV-018h0AvohNnSmBjgXlwhaPTIjg-8icORomE4Te0weyYHjmUW2Xa_PWSF_SvfgmHVmVosuHGeBBfhVCgv7gIX3byW6ae2P4iESfxs44omm_wXsTpaQMOVUt3iiUNR3BWH1oDqg-Rpzx20xCXJE6BpWHRzhW1fLIqRv-cQnoXzLbhhw5I2tLxDPErAMZPJSNg'}
        res = self.client().post('/api/categories', headers=self.headers,
                                 json={"name" : "This shouldn't work", "description" : "This shouldn't work"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'token_expired')

    ## 401 - Insufficient Permissions
    def test_insufficient_permissions(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWRmOTUxZGEyZDIzZjIwZThhZWU3NTU5IiwiYXVkIjoiY2hlYXRzaGVldCIsImlhdCI6MTU4NDA0NjgyMiwiZXhwIjoxNTg0MDU0MDIyLCJhenAiOiJ0SlFuR0o4Vlo4czFRcWJoY3ZFNWJiSEo5NEhRUXZFTyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.qgrFvQmxsvhkunJ03MzdpO-ySJN9R5M1Qb2wjisIsVR6UQXYRG_el2LhXus0bUTwF_vmfaWoCsckoB5NLESgtc8jWz5somE9cWP-Yg-gd019GFBUBUeZQ10vFh0jnQZqHAajUVVDbtPM_k48hAZKLTm2pxq0n9QSjxjxoNJD1OGx4kVJcJSbjrzPq74cL3B8RW3uz3q6kF8rUEmLCKSj7Nwtt_3HUVYJcUctiIWh_7DpQvqdX9tbzWpOY0Cis5iRyMklZUvk3n3xgvjPo-dShoJohPBProWJb3gG0HgZquHT_cfVzphDe-beTssuPZpoRlKrzmU0EieDIT1_zZ7nRw'}
        res = self.client().post('/api/categories', headers=self.headers,
                                 json={"name" : "This shouldn't work", "description" : "This shouldn't work"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    ## 404
    def test_get_nonexistent_page(self):
        res = self.client().get('/api/thispageforsuredoesntexist')

        self.assertEqual(res.status_code, 404)

    ## 405
    def test_method_not_allowed(self):
        res = self.client().get('/api/categories/1/update')

        self.assertEqual(res.status_code, 405)

    # def test_post_category(self):
    #     res = self.client().post(
    #         '/api/questions',
    #         json={"question": "What was Einsteins famous equation",
    #             "answer": "E=MC2",
    #             "category": 1,
    #             "difficulty": 2})
    #     data = json.loads(res.data)
    #    self.assertEqual(res.status_code, 200)  # Ensure successful request
    #     self.assertTrue(data['success'])  # Ensure JSON response was successful
    #     # Ensure posted data persisted in DB
    #     questions = Question.query.all()
    #     # There should now be 2 questions in db
    #     self.assertEqual(len(questions), 2)

    # def test_post_question_with_bad_input(self):
    #     res = self
    #         .client()
    #         .post(
    #             '/api/questions',
    #             json={
    #                 "question": "What was Einsteins famous equation"
    #             }
    #         )
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)  # Ensure successful request
    #     # Ensure JSON response was successful
    #     self.assertFalse(data['success'])
    #     # Ensure posted data persisted in DB
    #     questions = Question.query.all()
    #     # There should still only be 1 question in db
    #     self.assertEqual(len(questions), 1)

    # def test_get_paginated_questions(self):
    #     res = self.client().get('/api/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])

    # def test_get_categories(self):
    #     res = self.client().get('/api/categories')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertGreater(data['total_categories'], 0)

    # def test_delete_question(self):
    #     res = self.client().delete('/api/questions/1')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     # Verify that question with id=1 was in fact deleted
    #     self.assertEqual(data['request']['id'], 1)
    #     # Ensure posted data persisted in DB
    #     questions = Question.query.all()
    #     # There should now be 0 questions in db
    #     self.assertEqual(len(questions), 0)

    # def test_delete_invalid_question(self):
    #     res = self.client().delete('/api/questions/5000')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     # Ensure that success response is False
    #     self.assertFalse(data['success'])

    # def test_search_questions(self):
    #     res = self.client().post('/api/questions/search',
    #                              json={"searchTerm": "Alexander"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['total_questions'], 1)

    # def test_search_questions_with_no_questions(self):
    #     res = self.client().post('/api/questions/search',
    #                              json={"searchTerm": "Doesn't Exist"})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['total_questions'], 0)

    # def test_play(self):
    #     res = self.client().post('/api/play', json={"quizCategory": 1})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['question']['id'], 1)

    # def test_play_with_no_questions(self):
    #     res = self.client().post('/api/play', json={"quizCategory": 2})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertFalse(data['question'])

    # def test_get_category_questions(self):
    #     res = self.client().get('/api/categories/1/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     self.assertEqual(data['total_questions'], 1)

    # def test_get_category_questions_with_no_questions(self):
    #     res = self.client().get('/api/categories/2/questions')
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)
    #     self.assertTrue(data['success'])
    #     # No questions exist for category 2
    #     self.assertEqual(data['total_questions'], 0)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
