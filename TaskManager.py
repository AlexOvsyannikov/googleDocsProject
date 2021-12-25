class TaskManager:
    def __init__(self):
        self.all_tasks = []
        self.task_indexer = {}

    def put(self, _id, task):
        self.all_tasks.append(task)
        self.task_indexer[_id] = self.all_tasks.index(task)

    def get(self, _id):
        _ind = self.task_indexer.get(_id, 0)
        if not _ind:
            raise ValueError("TASK NOT FOUND")
        else:
            return self.all_tasks[_ind]

    def remove(self, _id):
        _ind = self.task_indexer.get(_id, 0)
        if not _ind:
            raise ValueError("TASK NOT FOUND")
        else:
            self.task_indexer[_id] = None
            self.all_tasks[_ind] = None
