from asyncio import sleep

from flask import Flask, render_template, request, jsonify, redirect

from TaskManager import Task, TaskManager
from formsParser import RequestSender, Parser, DataSender, AsyncDataSender
from hashlib import sha256

app = Flask(__name__, template_folder='template', static_folder='static')
sessions = {}
task_manager = TaskManager()


def connect_answers_and_probs(options, probs):
    form = []
    _count = 0
    for i in range(len(options)):
        _l = []
        for j in range(len(options[i])):
            _l.append(int(probs[_count]))
            _count += 1
        form.append(_l)
    return form


def make_suitable_format(options, probs):
    print(options)
    _poll = []
    for i in range(len(options)):
        _answer = []
        for j in range(len(options[i])):
            _answer.append({
                "name": options[i][j]['option'],
                "amount": probs[i][j],
                "text": None if not options[i][j]['free_type_answer'] else 'text.provided_data:rest;'
            })
        _poll.append(_answer)
    print(_poll)
    return _poll


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
    req = request.get_json()
    getter_of_data = RequestSender(sessions[req['session']])
    parser = Parser(sender=getter_of_data)
    parser.parse_title()
    parser.parse_description()
    parser.parse_script()
    parser.parse_questions()
    parser.parse_options()
    probs = connect_answers_and_probs(options=parser.options, probs=req['data'])
    answers = make_suitable_format(options=parser.options, probs=probs)
    sender = AsyncDataSender(parser=parser, max_time_to_sleep=int(req['sleep']),
                             num_of_votes=int(req['votes']),
                             list_of_answers=answers)

    task = Task(sender)
    _process_id = sha256(str(answers).encode()).hexdigest()
    task_manager.put(_process_id, task)
    task.start()
    return _process_id


@app.route('/id/<_id>')
def get_process(_id):
    try:
        _task = task_manager.get(_id)
    except ValueError:
        return render_template('not_found.html'), 404

    return render_template('process_page.html',
                           title=_task.name)


if __name__ == '__main__':
    app.run()
