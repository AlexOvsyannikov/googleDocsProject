from asyncio import sleep

from formsParser import AsyncDataSender


class Task:
    def __init__(self, sender: AsyncDataSender):
        self.sender = sender
        self.name = sender.parser.title

    def check_alive(self):
        return self.sender.check_alive()

    def start(self):
        self.sender.get_probs_of_answers()
        self.sender.get_naked_options()
        self.sender.work()


class TaskManager:
    def __init__(self):
        self.all_tasks = []
        self.task_indexer = {}

    def put(self, _id, task: Task):
        self.all_tasks.append(task)
        self.task_indexer[_id] = self.all_tasks.index(task)

    def get(self, _id):
        _ind = self.task_indexer.get(_id, -1)
        # print('###')
        # print(_id)
        # print(self.task_indexer)
        # print(self.all_tasks)
        # print('###')
        if _ind == -1:
            raise ValueError("TASK NOT FOUND")
        else:
            return self.all_tasks[_ind]

    def remove(self, _id):
        _ind = self.task_indexer.get(_id, 0)
        if not _ind:
            print(self.task_indexer)
            raise ValueError("TASK NOT FOUND")
        else:
            self.task_indexer[_id] = None
            self.all_tasks[_ind] = None
