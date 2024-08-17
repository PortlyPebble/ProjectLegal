from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
import search
import argparse

views = Blueprint('views', __name__, static_folder='static', template_folder='templates')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    search.query_rag(query_text)

@views.route('/ask', methods=['POST'])
def ask():
    data = request.json
    text = data.get('text', '')
    response = search.query_rag(text)
    return jsonify({'response': response})

@views.route('/', endpoint='home')
def home():
    return render_template('index.html', name="bob")

@views.route('/settings', endpoint='settings')
def settings():
    return render_template('settings.html', time=datetime.now())

if __name__ == "__main__":
    main()
