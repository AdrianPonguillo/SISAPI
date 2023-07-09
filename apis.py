from flask import Flask, jsonify, send_from_directory, request
import os

app = Flask(__name__)
PATH = os.path.join(os.path.dirname(__file__), 'files')
sent_files = set()

@app.route('/get_file', methods=['GET'])
def get_first_file():
    for file_name in os.listdir(PATH):
        if file_name.endswith('.json') and not os.path.isdir(os.path.join(PATH, file_name)) and file_name not in sent_files:
            sent_files.add(file_name)
            return send_from_directory(PATH, file_name, as_attachment=True)
    return jsonify({"message": "No .json file found in the directory or all files have been sent."})

@app.route('/delete_file', methods=['POST'])
def delete_file():
    file_name = request.json.get('file_name', None)
    if file_name:
        try:
            os.remove(os.path.join(PATH, file_name))
            sent_files.discard(file_name)
            return jsonify({"message": f"File {file_name} has been deleted."})
        except OSError:
            return jsonify({"message": f"File {file_name} not found."})
    return jsonify({"message": "No filename provided."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
