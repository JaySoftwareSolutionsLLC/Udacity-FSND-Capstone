import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin

from models import setup_db, Category, db


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

    @app.route('/categories', methods=['GET'])
    def display_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return render_template('categories.html', cats=formatted_categories)

    @app.route('/categories/<int:category_id>', methods=['GET'])
    def display_cheatsheet(category_id):
        cat = Category.query.get(category_id)
        formatted_cat = cat.format()
        return render_template('cheatsheet.html', cat=formatted_cat)

    ''' 
    API ENDPOINTS
    '''
    @app.route('/api/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]
        return jsonify({
            "success": True,
            "categories": formatted_categories,
            "total_categories": len(formatted_categories)
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

    @app.route('/api/categories/<int:category_id>', methods=['DELETE'])
    def delete_category(category_id):
        response = {}
        category_to_delete = Category.query.get(category_id)
        try:
            response['request'] = category_to_delete.format()
            db.session.delete(category_to_delete)
            db.session.commit()
            response['success'] = True
        except:
            db.session.rollback()
            response['success'] = False
        finally:
            db.session.close()
            return jsonify(response)

    @app.route('/api/categories/<int:category_id>', methods=['GET'])
    def get_category_info(category_id):
        response = {}
        cat = Category.query.get(category_id)
        try:
            response['category'] = cat.format()
            response['success'] = True
        except:
            response['success'] = False
        finally:
            return jsonify(response)


    return app

app = create_app()

if __name__ == '__main__':
    app.run()

# Need to run "export EXCITED=true" or "export EXCITED=false" AND "export DATABASE_URL=sqlite:///app.db" OR "postgres://postgres:$u944jAk161519@localhost:5432/udacity_fsnd_capstone" before running app locally