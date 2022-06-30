# import flask
# from flask import request, jsonify

# app = flask.Flask(__name__)
# app.config["DEBUG"] = True

# # Create some test data for our catalog in the form of a list of dictionary
# books = [
#     {
#         'id': 1,
#         'template_name': ' Template 1',
#         'subject': 'First Subject',
#         'body':'first subject body'
#     },
#     {
#         'id': 2,
#         'template_name': ' Template 2',
#         'subject': 'second Subject',
#         'body':'second subject body'
#     }
# ]

# @app.route('/', methods=['GET'])

# def home():
#     return "<h1>Distant Reading Archive</h1>"
# # A route to return all the template
# @app.route('/api/v1/template', methods=['GET'])
# def templates():
#     return jsonify(books)

# # @app.route('/register', methods=['GET'])

# # def register():
# #     return "<h1>this is registration page</h1>"

# app.run()
