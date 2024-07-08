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