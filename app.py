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
            new_category.insert()
            response['request'] = new_category.format()
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
        try:
            category_to_delete = Category.query.get(category_id)
            category_to_delete.delete()
            response['request'] = category_to_delete.format()
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

    @app.route('/api/categories/<int:category_id>/edit', methods=['PATCH'])
    def edit_category(category_id):
        response = {}
        try:
            name = request.json['name']
            description = request.json['description']
            cat = Category.query.get(category_id)
            cat.name = name
            cat.description = description
            cat.update()
            response['category'] = cat.format()
            response['success'] = True
        except:
            db.session.rollback()
            response['success'] = False
        finally:
            db.session.close()
            return jsonify(response)

    '''
    ERROR CODES
    '''

    # Forbidden
    @app.errorhandler(403)
    def not_found_error(error):
        error_code = 403
        error_msg = error
        return render_template('errors/error.html', response={"errorCode" : error_code, "errorMsg" : error_msg}), 403

    # Not found
    @app.errorhandler(404)
    def not_found_error(error):
        error_code = 404
        error_msg = error
        return render_template('errors/error.html', response={"errorCode" : error_code, "errorMsg" : error_msg}), 404

    # Method not allowed
    @app.errorhandler(405)
    def not_found_error(error):
        error_code = 405
        error_msg = error
        return render_template('errors/error.html', response={"errorCode" : error_code, "errorMsg" : error_msg}), 405

    # Internal server error
    @app.errorhandler(500)
    def not_found_error(error):
        error_code = 500
        error_msg = error
        return render_template('errors/error.html', response={"errorCode" : error_code, "errorMsg" : error_msg}), 500


    return app

app = create_app()

if __name__ == '__main__':
    app.run()

# Need to run "export EXCITED=true" or "export EXCITED=false" AND "export DATABASE_URL=sqlite:///app.db" OR "postgres://postgres:$u944jAk161519@localhost:5432/udacity_fsnd_capstone" before running app locally