import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "Question",
            "answer": "Answer",
            "difficulty": 2,
            'category': 1
        }

        self.search = {
            "searchTerm": "I Know Why the Caged Bird Sings"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories_200(self):
        res = self.client().get("/api/v1/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_get_categories_404(self):
        res = self.client().get("/api/v1/categories/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_get_questions_200(self):
        res = self.client().get("/api/v1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(len(data["categories"]))
        self.assertEqual(data["current_category"], None)

    def test_get_questions_404(self):
        res = self.client().get("/api/v1/questions?page=10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    # Delete a different question in each attempt
    def test_delete_question_200(self):
        res = self.client().delete("/api/v1/questions/19")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question_422(self):
        res = self.client().delete("/api/v1/questions/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Entity")

    def test_post_question_create_200(self):
        res = self.client().post("/api/v1/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_question_create_405(self):
        res = self.client().post("/api/v1/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method Not Allowed")

    def test_post_question_search_200(self):
        res = self.client().post("/api/v1/questions", json=self.search)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(data["current_category"], None)

    def test_post_question_search_400(self):
        res = self.client().post("/api/v1/questions", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad Request")

    def test_get_questions_by_categories_200(self):
        res = self.client().get("/api/v1/categories/2/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["current_category"])

    def test_get_questions_by_categories_404(self):
        res = self.client().get("/api/v1/categories/10000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource Not Found")

    def test_get_quiz_200_with_no_previous_questions(self):
        res = self.client().post("/api/v1/quizzes", json={
            "previous_questions": [],
            "quiz_category": {
                'id': '6',
                'type': 'Sports'
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["question"]))

    def test_get_quiz_200_with_some_previous_questions(self):
        res = self.client().post("/api/v1/quizzes", json={
            "previous_questions": [10],
            "quiz_category": {
                'id': '6',
                'type': 'Sports'
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["question"]))

    def test_get_quiz_200_with_all_previous_questions(self):
        res = self.client().post("/api/v1/quizzes", json={
            "previous_questions": [10,11],
            "quiz_category": {
                'id': '6',
                'type': 'Sports'
            }
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['question'], None)

    def test_get_quiz_422(self):
        res = self.client().post("/api/v1/quizzes", json={
            "previous_questions": [],
            "quiz_category": {}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Entity")

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()