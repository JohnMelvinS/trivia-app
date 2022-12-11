import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS"
        )
        return response

    # Route that retrieves all categories.
    # JSON Response body keys: 'success' and 'categories'
    @app.route('/api/v1/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        categoriesDict = {}
        for category in categories:
            categoriesDict[category.id] = category.type

        return jsonify({
            "success": True,
            "categories": categoriesDict
        })

    # Route that retrieves all questions.
    # JSON Response body keys: 'success', 'questions', 'total_questions', 'categories' and 'current_category'
    @app.route('/api/v1/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        categories = Category.query.order_by(Category.id).all()
        categoriesDict = {}
        for category in categories:
            categoriesDict[category.id] = category.type

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(questions),
            "categories": categoriesDict,
            "current_category": None
        })

    # Route that will delete a question.
    # JSON Response body keys: 'success'
    @app.route('/api/v1/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                "success": True
            })

        except:
            abort(422)

    # Route that will search.
    # JSON Response body keys: 'success', 'questions', 'total_questions' and 'current_category'
    # Route that will create a new question.
    # JSON Response body keys: 'success'
    @app.route('/api/v1/questions', methods=['POST'])
    def post_question():
        body = request.get_json()

        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        query = body.get('searchTerm', None)

        if query:
            try:
                # Search the term
                questions = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(query)))
                formatted_questions = [question.format() for question in questions]
                return jsonify({
                    'success': True,
                    'questions': formatted_questions,
                    'total_questions': len(questions.all()),
                    'current_category': None
                })
            except Exception:
                abort(422)
        else:
            if new_question and new_answer and new_category and new_difficulty:
                try:
                    question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                    question.insert()
                    return jsonify(
                        {
                            "success": True
                        }
                    )
                except:
                    abort(422)
            else:
                abort(400)

    # Route that retrieves all questions based on category
    # Response body keys: 'success', 'created'(id of created question), 'questions', 'total_questions' and 'current_category'
    @app.route('/api/v1/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        questions = Question.query.filter(Question.category == category_id).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(questions),
            "current_category": category_id
        })

    @app.route('/api/v1/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()
        quiz_category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')

        try:
            if (quiz_category['id'] == 0):
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == quiz_category['id']).all()

            available_questions = []
            for q in questions:
                if not q.id in previous_questions:
                    available_questions.append(q.id)
            
            if not available_questions:
                return jsonify({
                    'success': True,
                    'question': None
                })
            else:
                random_idx = random.choice(available_questions)
                print(random_idx)

                next_question = Question.query.filter(Question.id == random_idx).one_or_none()
                return jsonify({
                    'success': True,
                    'question': next_question.format()
                })

        except Exception as e:
            abort(422)


    """
    Error Handlers
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    return app