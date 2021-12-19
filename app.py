from flask import Flask, render_template, request, jsonify

from formsParser import RequestSender, Parser

app = Flask(__name__, template_folder='template', static_folder='static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start')
def start_form():
    return render_template('enter_form.html')


@app.route('/getForm', methods=['POST'])
def get_form():
    url = request.get_json()['url']
    getter_of_data = RequestSender(url)
    parser = Parser(sender=getter_of_data)
    parser.parse_title()
    parser.parse_description()
    parser.parse_script()
    parser.parse_questions()
    parser.parse_options()
    response = {
        "title": parser.title,
        "description": parser.description,
        "questions": parser.questions,
        "options": parser.options
    }
    print(response)
    return jsonify(response)

if __name__ == '__main__':
    app.run()