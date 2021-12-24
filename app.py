from flask import Flask, render_template, request, jsonify, redirect

from formsParser import RequestSender, Parser
from hashlib import sha256

app = Flask(__name__, template_folder='template', static_folder='static')
sessions = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start')
def start_form():
    if request.args.to_dict() != {}:
        return redirect('/start')
    return render_template('enter_form.html')


@app.route('/getForm', methods=['POST'])
def get_form():
    url = request.get_json()['url']
    _hash = sha256(url.encode()).hexdigest()
    sessions[_hash] = url
    getter_of_data = RequestSender(url)
    parser = Parser(sender=getter_of_data)
    parser.parse_title()
    parser.parse_description()
    parser.parse_script()
    parser.parse_questions()
    parser.parse_options()
    parser.parse_if_essential()
    response = {
        "title": parser.title,
        "description": parser.description,
        "questions": parser.questions,
        "options": parser.options
    }
    html = render_template('form-template.html',
                           title=response['title'],
                           description=response['description'],
                           questions=response['questions'],
                           options=response['options'],
                           session=_hash)
    return html


@app.route('/getProbes', methods=["POST"])
def get_probes():
    print(request.get_json())
    return 'okl'


if __name__ == '__main__':
    app.run()