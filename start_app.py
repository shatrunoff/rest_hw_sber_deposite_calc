from flask import Flask, request, jsonify
from deposite.validation_and_calculation import aggregate_validation_and_calculating

app = Flask(__name__)



@app.route('/deposite', methods=['POST'])
def proces_json():
    json_data = request.json
    if not aggregate_validation_and_calculating(json_data)[0]:
        return jsonify(aggregate_validation_and_calculating(json_data)[1]), 400
    
    return jsonify(aggregate_validation_and_calculating(json_data)[1]), 200



if __name__ == '__main__':
    app.run(debug=True)