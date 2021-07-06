import random
from abc import ABC, abstractmethod
import json
from time import sleep

import requests
from bs4 import BeautifulSoup


# https://docs.google.com/forms/d/1SHrWtckuShjPA8npdVEBFGzF4FTJbUsgagrxr92sD7g/viewform?edit_requested=true


class AbstractRequestSender(ABC):
    def __init__(self, url):
        self.url = url

    # gets data from url
    @abstractmethod
    def request_data(self):
        pass


class RequestSender(AbstractRequestSender):
    # returns text from request
    def request_data(self):
        return requests.get(self.url).text


class Parser:
    def __init__(self, url: str, sender: AbstractRequestSender):
        self.url = url
        self.soup = BeautifulSoup(sender.request_data(), 'lxml').find('body')
        self.title = None
        self.description = None
        # list of data about form (all options and questions)
        self.data = []
        # list of questions, None if no name
        self.questions = []
        # list of options
        self.options = []
        # list of ints, entities, used for requests
        self.entities = []

    def parse_title(self):
        """Gets title of form from html"""
        try:
            self.title = self.soup.find('div', attrs='freebirdFormviewerViewHeaderTitle').string
        except:
            self.description = "Impossible to parse"

    def parse_description(self):
        """Gets description of form from html"""
        try:
            self.description = self.soup.find('div', attrs='freebirdFormviewerViewHeaderDescription').string
        except:
            self.description = "Impossible to parse"

    def parse_script(self):
        """Gets list of data from html"""
        __script = self.soup \
                       .find("script") \
                       .string \
                       .split("=")[-1] \
                       .replace("null", '"None"') \
                       .replace(";", "") \
                       .replace("\n", "") \
                       .split(',"/forms"')[0] \
                       .strip() \
                   + "]"

        self.data = json.loads(__script)[1][1]

    def parse_questions(self):
        """Gets questions from data"""
        for i in self.data:
            if len(i) > 4:
                self.questions.append(i[1])

    def parse_options(self):
        """Gets entities and options from data"""
        for question in self.data:
            if len(question) > 4:
                try:
                    self.entities.append(question[-1][0][0])

                    # checks if any options are available
                    if question[-1][0][1] != "None":
                        __options_for_one_question = []
                        for answer in question[-1][0][1]:
                            __options_for_one_question.append({"option": answer[0],
                                                               "free_type_answer": answer[-1]})

                        self.options.append(__options_for_one_question)

                    else:
                        self.options.append([{"option": '',
                                              "free_type_answer": 1}])
                except:
                    self.entities.append("")
                    self.options.append([])
                    print("ERROR WITH THIS PARAMS ", question)


class DataSender:
    def __init__(self, parser: Parser, num_of_votes: int, max_time_to_sleep: int, list_of_answers: list,
                 mode="percent"):
        """
        :param parser:
        :param num_of_votes: number of votes that you need
        :param time_to_work: time in seconds to split time between answers
        :param list_of_answers:
        :param mode: ONLY PERCENT IS AVAILABLE
        """
        self.max_time_to_sleep = max_time_to_sleep
        self.mode = mode
        self.list_of_answers = list_of_answers
        self.num_of_votes = num_of_votes
        self.parser = parser
        self.probs = []
        self.naked_options = []
        self.provided_full_answers = {}
        self.url = self.parser.url.split("viewform")[0]

    def get_probs_of_answers(self):
        for answer in self.list_of_answers:
            __prob = []
            __name = []
            for option in answer:
                __prob.append(option["amount"])
                if option["name"] != '':
                    __name.append(option["name"])
                else:
                    __name.append(option["text"])

            self.probs.append(__prob)
            self.naked_options.append(__name)

    def send_data(self):
        print(self.num_of_votes)
        print("===========================")
        print(self.parser.questions)
        print("===========================")
        print(self.naked_options)
        print("===========================")
        print(self.probs)
        print("===========================")
        url = self.url + "formResponse"
        for vote in range(self.num_of_votes):
            data_to_send = {}
            for question_num in range(len(self.parser.questions)):
                try:
                    choice = random.choices(self.naked_options[question_num], weights=self.probs[question_num])[0]
                    if "text" not in choice:
                        data_to_send["entry." + str(self.parser.entities[question_num])] = choice

                    elif choice == "text.random":
                        print(choice)
                        data_to_send["entry." + str(self.parser.entities[question_num]) + ".other_option_response"] = \
                            ''.join(random. \
                                    choice('qwerйцукенгшщзхъфывапролджэёячсмитьбюЙЦУКЕНГШЩЗХЪ' +
                                           'ФЫВАПРОЛДЖЭЁЯЧСМИТЬБЮtyuiopasdfghjklzxQWERTYUIOPASDFGHJKLZXCVBNMcvbnm') for
                                    _ in range(20))
                        data_to_send["entry." + str(self.parser.entities[question_num])] = "__other_option__"

                    elif "text.provided_data:" in choice:
                        lines = choice.split("text.provided_data:")[1].strip()
                        if not self.provided_full_answers.get(question_num, 0):
                            self.provided_full_answers[question_num] = [line.strip() for line in lines.split(";") if line]

                        data_to_send["entry." + str(self.parser.entities[question_num]) + ".other_option_response"] \
                            = self.provided_full_answers[question_num].pop()
                        data_to_send["entry." + str(self.parser.entities[question_num])] = "__other_option__"
                        print(self.provided_full_answers)


                except Exception as e:
                    print("ERROR WITH THIS PARAMS ", self.parser.questions[question_num])
                    print(e)

            r = requests.post(url, data=data_to_send, headers={})

            __time_to_sleep = random.randint(0, self.max_time_to_sleep)
            if r.status_code == requests.codes.OK:
                print(f"ANSWER {vote + 1} PROVIDED")
            else:
                print("SOMETHING WRONG")
                print(r)
                print(r.text)
            print(f"SLEEPING FOR {__time_to_sleep} seconds")
            sleep(__time_to_sleep)


if __name__ == '__main__':
    url = "https://docs.google.com/forms/d/1SHrWtckuShjPA8npdVEBFGzF4FTJbUsgagrxr92sD7g/viewform?edit_requested=true"
    # url = 'https://docs.google.com/forms/d/1Yupf2u1NHP8-5XY_l0B0ZroLKAuqNuRuI1qn_gwVaW4/'
    getter_of_data = RequestSender(url)
    parser = Parser(url, getter_of_data)
    parser.parse_title()
    parser.parse_description()
    parser.parse_script()
    parser.parse_questions()
    parser.parse_options()

    sender = DataSender(parser=parser, max_time_to_sleep=1, num_of_votes=100, list_of_answers=[
        [
            {
                "name": "Вариант 1",
                "amount": 3,
                "text": None
            },
            {
                "name": "Вариант 2",
                "amount": 10,
                "text": None
            },
            {
                "name": "Вариант 3",
                "amount": 17,
                "text": None
            },
            {
                "name": "",
                "amount": 70,
                "text": "text.provided_data: Check;LOL;get_text;"
            }
        ],
        [
            {
                "name": "Вариант 1",
                "amount": 70,
                "text": None
            },
            {
                "name": "Вариант 2",
                "amount": 10,
                "text": None
            },
            {
                "name": "Вариант 3",
                "amount": 17,
                "text": None
            },
            {
                "name": "Вариант 4",
                "amount": 3,
                "text": None
            }
        ],
        [
            {
                "name": "Вариант 1",
                "amount": 70,
                "text": None
            },
            {
                "name": "Вариант 2",
                "amount": 10,
                "text": None
            },
            {
                "name": "Вариант 3",
                "amount": 17,
                "text": None
            }
        ]
    ])

    sender.get_probs_of_answers()
    sender.send_data()
