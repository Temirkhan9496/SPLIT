from flask import Flask, request, jsonify
import json
from models import PerevalDataHandler

app = Flask(__name__)
db_handler = PerevalDataHandler()


@app.route('/submitData', methods=['POST'])
def submit_data():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        date_added = data.get('date_added')
        raw_data = data.get('raw_data')
        images = data.get('images')

        if not date_added or not raw_data:
            return jsonify({"error": "Missing required fields"}), 400

        pereval_id = db_handler.add_pereval(date_added, raw_data, images)
        return jsonify({"message": "Pereval added", "pereval_id": pereval_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

# Добавление новых методов для REST API
app = Flask(__name__)
db_handler = DatabaseHandler()

@app.route('/submitData/<int:id>', methods=['GET'])
def get_pereval(id):
    try:
        record = db_handler.get_pereval_by_id(id)
        if record:
            return jsonify(record), 200
        else:
            return jsonify({"message": "Record not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@app.route('/submitData/<int:id>', methods=['PATCH'])
def update_pereval(id):
    try:
        data = request.json
        status, message = db_handler.update_pereval(id, data)
        return jsonify({"state": status, "message": message}), 200 if status == 1 else 400
    except Exception as e:
        return jsonify({"state": 0, "message": str(e)}), 500


@app.route('/submitData/', methods=['GET'])
def get_perevals_by_email():
    email = request.args.get('user__email')
    if email:
        try:
            records = db_handler.get_perevals_by_email(email)
            return jsonify(records), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    else:
        return jsonify({"message": "Email parameter is required"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('FSTR_PORT', 5000))

   #Обновим наш app.py для интеграции Swagger:

from flask import Flask, request, jsonify
from flasgger import Swagger
from db_handler import DatabaseHandler
import os

app = Flask(__name__)
swagger = Swagger(app)
db_handler = DatabaseHandler()

@app.route('/submitData/<int:id>', methods=['GET'])
def get_pereval(id):
    """
    Get Pereval by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the Pereval
    responses:
      200:
        description: Pereval found
        schema:
          id: int
          name: str
          height: int
          difficulty: str
          user_email: str
      404:
        description: Pereval not found
    """
    try:
        record = db_handler.get_pereval_by_id(id)
        if record:
            return jsonify(record), 200
        else:
            return jsonify({"message": "Record not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/submitData/<int:id>', methods=['PATCH'])
def update_pereval(id):
    """
    Update Pereval by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the Pereval
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            height:
              type: integer
            difficulty:
              type: string
    responses:
      200:
        description: Pereval updated
        schema:
          state: int
          message: str
      400:
        description: Bad request
      500:
        description: Internal Server Error
    """
    try:
        data = request.json
        status, message = db_handler.update_pereval(id, data)
        return jsonify({"state": status, "message": message}), 200 if status == 1 else 400
    except Exception as e:
        return jsonify({"state": 0, "message": str(e)}), 500

@app.route('/submitData/', methods=['GET'])
def get_perevals_by_email():
    """
    Get Perevals by Email
    ---
    parameters:
      - name: user__email
        in: query
        type: string
        required: true
        description: Email of the user
    responses:
      200:
        description: Perevals found
        schema:
          type: array
          items:
            id: int
            name: str
            height: int
            difficulty: str
            user_email: str
      400:
        description: Email parameter is required
      500:
        description: Internal Server Error
    """
    email = request.args.get('user__email')
    if email:
        try:
            records = db_handler.get_perevals_by_email(email)
            return jsonify(records), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 500
    else:
        return jsonify({"message": "Email parameter is required"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('FSTR_PORT', 5000))