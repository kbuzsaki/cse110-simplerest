import pprint
from flask import Flask, request
from datetime import datetime
import json

app = Flask(__name__)

pp = pprint.PrettyPrinter(indent=4)

@app.route('/')
def index():
    return "Hello World!"

NAMES = ["John", "Joe", "Sally", "Jake", "Jake", "Rob", "Max", "Spencer", "Pete", "Alec", "Mark"]

@app.route('/api/group/<int:group_id>')
def get_group(group_id):
    response = {"error": "illegal id"}

    if group_id == 3:
        response = {
            "id": 3,
            "name": "Bob's Group",
            "members": [2],
            "polls": [1, 2]
        }
    else:
        response = {
            "id": group_id,
            "name": NAMES[group_id] + "'s Group",
            "members": [2],
            "polls": []
        }

    return json.dumps(response)



@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    response = {"error": "illegal id"}

    if user_id == 1:
        response = {
            "id": user_id,
            "name": "Sally Forth",
            "groups": [0, 1, 2]
        }
    if user_id == 2:
        response = {
            "id": user_id,
            "name": "Joe User",
            "groups": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        }
    elif user_id == 3:
        response = {
            "id": user_id,
            "name": "John Doe",
            "groups": [0, 1, 2]
        }

    return json.dumps(response)

@app.route('/api/poll/<int:poll_id>')
def get_poll(poll_id):
    response = {"error": "illegal id"}

    if poll_id == 1:
        response = {
            "id": 1,
            "group": 1,
            "creator": 2,
            "created": datetime.now().isoformat(),
            "name": "Some Poll",
            "questions": [1, 2, 3, 4]
        }
    elif poll_id == 2:
        response = {
            "id": 2,
            "group": 1,
            "creator": 2,
            "created": datetime.now().isoformat(),
            "name": "Some Other Poll",
            "questions": [5]
        }

    return json.dumps(response)

def load_args(args):
    return {key: load_arg(value) for key, value in request.args.items()}

def load_arg(arg):
    if "[" in arg or "{" in arg:
        return json.loads(arg)
    elif arg.isdigit():
        return int(arg)
    else:
        return arg

@app.route('/api/poll/create', methods=["GET", "POST"])
def create_poll():
    args = load_args(request.args)
    pp.pprint(args)
    response = {
        "id": 3,
        "group": 1,
        "creator": 2,
        "created": datetime.now().isoformat(),
        "name": "Fake Poll",
        "questions": []
    }
    return json.dumps(response)

@app.route('/api/question/<int:question_id>')
def get_question(question_id):
    response = {"error": "illegal id"}

    if question_id == 1:
        response = {
            "id": 1,
            "poll": 1,
            "type": "choice",
            "title": "What pizza toppings?",
            "content": {
                "allow_multiple": True,
                "allow_custom": False,
                "options": [
                    "pepperoni",
                    "sausage",
                    "onion"
                ],
                "responses": [1, 2, 3]
            }
        }
    elif question_id == 2:
        response = {
            "id": 2,
            "poll": 1,
            "type": "choice",
            "title": "Who drives to get it?",
            "content": {
                "allow_multiple": False,
                "allow_custom": False,
                "options": [
                    "Mark",
                    "Sean",
                    "James"
                ]
            }
        }
    elif question_id == 3:
        response = {
            "id": 3,
            "poll": 1,
            "type": "choice",
            "title": "Cutest pet??",
            "content": {
                "allow_multiple": False,
                "allow_custom": False,
                "options": [
                    "Dog",
                    "Cat",
                    "Duck"
                ]
            }
        }
    elif question_id == 4:
        response = {
            "id": 4,
            "poll": 1,
            "type": "choice",
            "title": "Silliest pet??",
            "content": {
                "allow_multiple": True,
                "allow_custom": False,
                "options": [
                    "Pig",
                    "Bat",
                    "Bear"
                ]
            }
        }
    elif question_id == 5:
        response = {
            "id": 5,
            "poll": 2,
            "type": "choice",
            "title": "Cutest pet??",
            "content": {
                "allow_multiple": False,
                "allow_custom": False,
                "options": [
                    "Dog",
                    "Cat",
                    "Duck"
                ]
            }
        }

    choice_responses = [resp["id"] for resp in response_history if resp["question"] == response["id"]]
    response["content"]["responses"] = choice_responses

    return json.dumps(response)

@app.route('/api/response/<int:response_id>')
def get_response(response_id):
    reponse = {"error": "illegal id"}

    if response_id == 1:
        response = {
            "id": response_id,
            "question": 1,
            "responder": 1,
            "choices": ["pepperoni", "sausage"]
        }
    elif response_id == 2:
        response = {
            "id": response_id,
            "question": 1,
            "responder": 2,
            "choices": ["pepperoni"]
        }
    elif response_id == 3:
        response = {
            "id": response_id,
            "question": 1,
            "responder": 3,
            "choices": ["pepperoni"]
        }
    else:
        matches = [resp for resp in response_history if resp["id"] == response_id]
        if matches:
            response = matches[0]

    return json.dumps(response)

LAST_RESPONSE_ID = 3
response_history = []

@app.route('/api/response/create', methods=["GET", "PUT"])
def put_response():
    global LAST_RESPONSE_ID
    LAST_RESPONSE_ID += 1
    question_response = request.json["response"]
    response = {
        "id": LAST_RESPONSE_ID,
        "responder": int(question_response["responder"]),
        "question": int(question_response["question"]),
        "choices": list(question_response["choices"])
    }
    response_history.append(response)
    return json.dumps(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")


