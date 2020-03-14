import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify
from app import create_app
from models import setup_db, db, Category, Topic, Concept

from auth.auth import get_token_auth_header

expired_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDIwNzY1MTYxMjg2ODU5MTEwNDQiLCJhdWQiOlsiY2hlYXRzaGVldCIsImh0dHBzOi8vYmpiLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODM5NjUxMTUsImV4cCI6MTU4Mzk3MjMxNSwiYXpwIjoidEpRbkdKOFZaOHMxUXFiaGN2RTViYkhKOTRIUVF2RU8iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.qxx27bvY5SFrHWrsjVTuOKyYTnvqWZU9dLa8EGcHqX_Qgk6u5Mi4TfWmjoWx1VFEyuuvJ1EkArAqe_6LymIkrAjsouBVuqym1N6_MrG7O4JrgILKqj6rkIhPXpAXluhYBgd3isbWKtOHDaoycYEqaV-018h0AvohNnSmBjgXlwhaPTIjg-8icORomE4Te0weyYHjmUW2Xa_PWSF_SvfgmHVmVosuHGeBBfhVCgv7gIX3byW6ae2P4iESfxs44omm_wXsTpaQMOVUt3iiUNR3BWH1oDqg-Rpzx20xCXJE6BpWHRzhW1fLIqRv-cQnoXzLbhhw5I2tLxDPErAMZPJSNg'
teacher_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2ZDIyZGExMDg4NWIwY2E2YTg1NjllIiwiYXVkIjoiY2hlYXRzaGVldCIsImlhdCI6MTU4NDIxMDc5MiwiZXhwIjoxNTg0Mjk3MTkyLCJhenAiOiJ0SlFuR0o4Vlo4czFRcWJoY3ZFNWJiSEo5NEhRUXZFTyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFueSIsImRlbGV0ZTphbnkiLCJ1cGRhdGU6YW55Il19.KDtic9q5Nr07pxnIDnRcFz6qizZYZeUQwHT91EAMiUlUvaT7sW0hDZZp4ZS_55csYlDpADKDMJ1Kt0AkKnyz7bX6-Ttc-91OdGTGKF3ARpXuaQOCxiqJaM_zqmiTkdNB4dxaCS2FBXdY6RToxChcNaxd4vcz3CZHoWRr5THSMkRffjS1k23Y9p2q4X09y3zrXE64-o9T_BJs7vqyerDGfv06qq6_7iJLRVGTzFHqB8odN0E0EaaHXs91fNAbAncy11FS8ccreIc3XVLzqdL8DHT5HNJ1Tcfd1MBSFLWob6QilszOcYuMBMS7-oLk8h2HrGwRIWBrGhM4Q-whsSokGA'
student_jwt = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJFWXpNVVJDT0RBMU16RTRNak5DTVRBd056Y3dOVEU1TmpNME9VSkVSVGM0UmpjelJqTXhNdyJ9.eyJpc3MiOiJodHRwczovL2JqYi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU2ZDIyOTAwODQ1NzEwYzkyMjE0OGUzIiwiYXVkIjoiY2hlYXRzaGVldCIsImlhdCI6MTU4NDIxMTE0NSwiZXhwIjoxNTg0Mjk3NTQ1LCJhenAiOiJ0SlFuR0o4Vlo4czFRcWJoY3ZFNWJiSEo5NEhRUXZFTyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOltdfQ.JJDIBm5x9KiZxCOpp4HDYl5Rcduz3XgxTBLEyyNfMUuZlUfrx-HiH6gEoAlC5RHDlIdcJJad5whL1sgePJ43RZZRZS5gHruxAGl-mw1x4rbWQG3P16yRpX9zIHOJ0IRE98zsXxoNL1NdCthkh22RhCFHkquSxwPMBtRGKriGQHLFEWKFUWjlSoZeQW0gnjR33R7hTfkqejVhIYCJ7u1szB2gJL7E3KVmFtdUHdOoPLWpPbGgkyuWpN7uoJ3Wg1iOK4HyGGBFzUKqTPU3spo0BM9k0rmyQn_8hDDrq5Dd1LFQuzP6gzq4WvHcgwca87S9iT-oGnfq2dC3rXBbfZpFnA'

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

    def tearDown(self):
        """Executed after reach test"""
        pass


    '''
    TESTS
    '''

    def test_always_true(self):
        self.assertTrue(True)

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

    # Comprehensive test for all of Category CRUD functionality
    def test_category_crud(self):
        # Create new category
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        res = self.client().post('/api/categories', headers=self.headers, json={"name" : "TestCat4", "description" : "This is a test category for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that data persisted in DB
        self.assertTrue(Category.query.get(data['category']['id']))

        # Edit the category
        res = self.client().patch('/api/categories/4/update', headers=self.headers, json={"name" : "TestCat4-E", "description" : "This is a test category for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that editted content now exists in DB
        editted_cat = Category.query.get(data['category']['id'])
        self.assertEqual(editted_cat.name, 'TestCat4-E')

        # Delete the category
        res = self.client().delete('/api/categories/4', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that row no longer exists in DB
        self.assertFalse(Category.query.get(data['category']['id']))

    def test_category_post_bad_request(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        # Passing JSON object without name should result in failure message
        res = self.client().post('/api/categories', headers=self.headers, json={"description" : "This is a test category for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])

    def test_category_patch_bad_request(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        # Passing JSON object without name should result in failure message
        res = self.client().patch('/api/categories/3/update', headers=self.headers, json={"description" : "This is a test category for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])

    def test_student_cannot_create_category(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().post('/api/categories', headers=self.headers, json={"name" : "TestCat4", "description" : "This is a test concept for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    def test_student_cannot_edit_category(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().patch('/api/categories/1/update', headers=self.headers, json={"name" : "TestCat1-E", "description" : "This is a test category for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    def test_student_cannot_delete_category(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().delete('/api/categories/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    # Comprehensive test for all of Topic CRUD functionality
    def test_topic_crud(self):
        # Create new topic
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        res = self.client().post('/api/topics', headers=self.headers, json={"name" : "TestTop4", "description" : "This is a test topic for testing purposes", "category_id" : 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that data persisted in DB
        self.assertTrue(Topic.query.get(data['topic']['id']))

        # Edit the topic
        res = self.client().patch('/api/topics/4/update', headers=self.headers, json={"name" : "TestTop4-E", "description" : "This is a test topic for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that editted content now exists in DB
        editted_cat = Topic.query.get(data['topic']['id'])
        self.assertEqual(editted_cat.name, 'TestTop4-E')

        # Delete the topic
        res = self.client().delete('/api/topics/4', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that row no longer exists in DB
        self.assertFalse(Topic.query.get(data['topic']['id']))

    def test_topic_post_bad_request(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        # Passing JSON object without name should result in failure message
        res = self.client().post('/api/topics', headers=self.headers, json={"description" : "This is a test topic for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])

    def test_topic_patch_bad_request(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        # Passing JSON object without name should result in failure message
        res = self.client().patch('/api/topics/3/update', headers=self.headers, json={"description" : "This is a test topic for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])

    def test_student_cannot_create_topic(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().post('/api/topics', headers=self.headers, json={"name" : "TestTop4", "description" : "This is a test concept for testing purposes", "category_id" : 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    def test_student_cannot_edit_topic(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().patch('/api/topics/1/update', headers=self.headers, json={"name" : "TestTop1-E", "description" : "This is a test topic for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    def test_student_cannot_delete_topic(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().delete('/api/topics/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    # Comprehensive test for all of Concept CRUD functionality
    def test_concept_crud(self):
        # Create new concept
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        res = self.client().post('/api/concepts', headers=self.headers, json={"name" : "TestCon4", "description" : "This is a test concept for testing purposes", "topic_id" : 1, "url" : "https://www.original_url.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that data persisted in DB
        self.assertTrue(Concept.query.get(data['concept']['id']))

        # Edit the concept
        res = self.client().patch('/api/concepts/4/update', headers=self.headers, json={"name" : "TestCon4-E", "description" : "This is a test concept for testing purposes", "url" : "https://www.modified_url.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that editted content now exists in DB
        editted_cat = Concept.query.get(data['concept']['id'])
        self.assertEqual(editted_cat.name, 'TestCon4-E')
        self.assertEqual(editted_cat.url, 'https://www.modified_url.com')

        # Delete the concept
        res = self.client().delete('/api/concepts/4', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

        # Verify that row no longer exists in DB
        self.assertFalse(Concept.query.get(data['concept']['id']))

    def test_concept_post_bad_request(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        # Passing JSON object without name should result in failure message
        res = self.client().post('/api/concepts', headers=self.headers, json={"description" : "This is a test concept for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])

    def test_concept_patch_bad_request(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(teacher_jwt) }
        # Passing JSON object without name should result in failure message
        res = self.client().patch('/api/concepts/3/update', headers=self.headers, json={"description" : "This is a test concept for testing purposes"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertFalse(data['success'])

    def test_student_cannot_create_concept(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().post('/api/concepts', headers=self.headers, json={"name" : "TestTop4", "description" : "This is a test concept for testing purposes", "topic_id" : 1, "url" : "https://www.test.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    def test_student_cannot_edit_concept(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().patch('/api/concepts/1/update', headers=self.headers, json={"name" : "TestCon1-E", "description" : "This is a test concept for testing purposes", "url" : "https://www.test.com"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')

    def test_student_cannot_delete_concept(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt) }
        res = self.client().delete('/api/concepts/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'insufficient_permissions')


    # Error code testing

    ## 401
    def test_unauthorized_user(self):
        res = self.client().post('/api/categories',
                                 json={"name" : "This shouldn't work", "description" : "This shouldn't work"})

        self.assertEqual(res.status_code, 401)

    ## 401 - Expired token
    def test_expired_token(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(expired_jwt)}
        res = self.client().post('/api/categories', headers=self.headers,
                                 json={"name" : "This shouldn't work", "description" : "This shouldn't work"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'token_expired')

    ## 401 - Insufficient Permissions
    def test_insufficient_permissions(self):
        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(student_jwt)}
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

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
