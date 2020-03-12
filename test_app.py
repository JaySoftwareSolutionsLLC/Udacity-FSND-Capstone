import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify
from app import create_app
from models import setup_db, db, Category, Topic, Concept

class TriviaTestCase(unittest.TestCase):
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
            #     "TRUNCATE categories, questions RESTART IDENTITY CASCADE")
            # # Create new category for DB
            # category1 = Category(type="Science")
            # if len(Category.query.all()) == 0:
                # self.db.session.add(category1)
                # self.db.session.commit()
            # Create new question for DB
            # To adhere to PEP8 how do we keep these lines below 79 characters?
            # question1 = Question(question="What did Alexander Fleming discover"
                                # , answer="Penicillin"
                                # , category="1"
                                # , difficulty=2)  
            # if len(Question.query.all()) == 0: 
                # self.db.session.add(question1)
                # self.db.session.commit()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    WIP
    Write at least one test for each test for 
    successful operation and for expected errors.
    """

    def test_always_true(self):
        self.assertTrue(True)

    # def test_post_question(self):
    #     res = self.client().post(
    #         '/api/questions',
    #         json={"question": "What was Einsteins famous equation",
    #             "answer": "E=MC2",
    #             "category": 1,
    #             "difficulty": 2})
    #     data = json.loads(res.data)

    #     self.assertEqual(res.status_code, 200)  # Ensure successful request
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
