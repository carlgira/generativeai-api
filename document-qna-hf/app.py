import os
from flask import Flask, request, jsonify
from hf_langchain import OpenSearchBackend


flask = Flask(__name__)

OPENSEARCH_URL = os.environ['OPENSEARCH_URL']
backed = OpenSearchBackend(OPENSEARCH_URL)


@flask.route('/load_file', methods=['POST'])
def load_file():
    file = request.files['document']
    file_name = file.filename
    index_name = file_name
    if request.get_json().has_key('index'):
        index_name = request.get_json()['index']
    
    if not os.path.isdir(file_name):
        file.save(file_name)

    docs = backed.read_document(file_name)
    backed.load_doc_to_db(docs, opensearch_index=index_name, verify_certs=False)

    return jsonify({"status": "file loaded", "index": index_name})


@flask.route('/query_docs', methods=['POST'])
def query_docs():
    question = request.get_json()['question']
    index_name = request.get_json()['index']

    return jsonify({"response" : backed.answer_query(question, opensearch_index=index_name, verify_certs=False)})


if __name__ == '__main__':
    flask.run(host='0.0.0.0', port=3000)
