import os
from flask import Flask, request, jsonify
from models import setup_db, Category, db
from flask_cors import CORS, cross_origin



def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    # CORS(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def get_greeting():
        excited = os.environ['EXCITED']
        greeting = "Hello" 
        if excited == 'true': greeting = greeting + "!!!!!"
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool! You're almost a FSND grad!"

    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        return jsonify({
            "success": True
        })

    @app.route('/api/categories', methods=['POST'])
    def create_category():
        response = {}
        try:
            name = request.json['name']
            description = request.json['description']
            new_category = Category(
                name=name, description=description)
            response['request'] = new_category.format()
            db.session.add(new_category)
            db.session.commit()
            response['success'] = True
        except:
            db.session.rollback()
            response['success'] = False
        finally:
            db.session.close()
            return jsonify(response)


    return app

app = create_app()

if __name__ == '__main__':
    app.run()

# Need to run "export EXCITED=true" or "export EXCITED=false" AND "export DATABASE_URL=sqlite:///app.db" OR "postgres://postgres:$u944jAk161519@localhost:5432/udacity_fsnd_capstone" before running app locally