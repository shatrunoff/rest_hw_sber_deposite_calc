from flask import Flask, request, jsonify, Response
from deposite.validation_and_calculation import aggregate_validation_and_calculating
import json

app = Flask(__name__)



@app.route('/deposite', methods=['POST'])
def proces_json():
    json_data = request.json

    if not aggregate_validation_and_calculating(json_data)[0]:
        return jsonify(aggregate_validation_and_calculating(json_data)[1]), 400
    
    response_data = aggregate_validation_and_calculating(json_data)[1]
    response_json = json.dumps(response_data, ensure_ascii=False, sort_keys=False)
    
    return Response(response_json, mimetype='application/json'), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)
