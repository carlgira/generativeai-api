import os
from flask import Flask, request, jsonify
from cohere_langchain import OpenSearchBackend


flask = Flask(__name__)

OPENSEARCH_URL = os.environ['OPENSEARCH_URL']
backed = OpenSearchBackend(OPENSEARCH_URL)

APP_INDEX_PREFIX ='co_'

@flask.route('/load_file', methods=['POST'])
def load_file():
    file = request.files['document']
    index_name = APP_INDEX_PREFIX + request.form.get('index')

    file_name = file.filename
    
    if not os.path.isdir(file_name):
        file.save(file_name)

    docs = backed.read_document(file_name)
    backed.load_doc_to_db(docs, opensearch_index=index_name, verify_certs=False)

    return jsonify({"status": "file loaded", "index": request.get_json()['index']})


@flask.route('/query_docs', methods=['POST'])
def query_docs():
    question = request.get_json()['question']
    index_name = APP_INDEX_PREFIX + request.form.get('index')

    return jsonify({"response" : backed.answer_query(question, opensearch_index=index_name, verify_certs=False)})


if __name__ == '__main__':
    flask.run(host='0.0.0.0', port=3000)

