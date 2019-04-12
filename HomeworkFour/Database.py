import pymongo as pm
import unittest

# Responsible for holding task data
class Task:
    def __init__(self, name = "", deadline = 0, description = "", members = [], task = None):
        if task == None:
            self.__name = name
            self.__deadline = deadline
            self.__description = description
            self.__members = members
        else:
            self.__name = task["name"]
            self.__deadline = task["deadline"]
            self.__description = task["description"]
            self.__members = task["members"]

    def get_json(self):
        return {"name": self.__name, "deadline": self.__deadline, "description": self.__description, "members": self.__members}

    def __str__(self):
        return self.get_json().__str__()

    def __repr__(self):
        return self.__str__()

# Responsible for keeping track of its tasks
class Project:
    def __init__(self, name = "", deadline = 0, description = "", members = [], project = None):
        self.__tasks = []
        if project == None:
            self.__name = name
            self.__deadline = deadline
            self.__description = description
            self.__members = members
        else:
            self.__tasks = [Task(task = json) for json in project["tasks"]]
            self.__name = project["name"]
            self.__deadline = project["deadline"]
            self.__description = project["description"]
            self.__members = project["members"]

    def add_task(self, task):
        self.__tasks.append(task)

    def remove_task(self, task):
        self.__tasks.remove(task)

    def get_tasks(self):
        return self.__tasks

    def get_name(self):
        return self.__name

    # Used to easily save into the mongodb database
    def get_json(self):
        tasks = [task.get_json() for task in self.__tasks]
        json = {"tasks" : tasks, "name": self.__name, "deadline": self.__deadline, "description": self.__description, "members": self.__members}
        return json

    def __str__(self):
        return self.get_json().__str__()

    def __repr__(self):
        return self.__str__()

class Subject:
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self):
        for observer in self.__observers:
            observer.update()

# Responsible for managing all of the project through the database
class Database(Subject):
    __instance = None

    def __init__(self):
        Subject.__init__(self)
        if Database.__instance != None: # Prevents more than one instance of the singleton from occurring
            raise Exception("Attempt to more than one Database singleton instance.")
        
        Database.__instance = self
        db_server = pm.MongoClient("mongodb://localhost:27017/")
        the_database = db_server["project_database"]
        self.__saved_projects = the_database["projects"]

    @staticmethod
    def get_instance(): # Can be accessed anywhere to get the instance of database
        if Database.__instance == None:
            Database() # Call the constructor it instantiate an instance
        return Database.__instance

    def get_projects(self):
        return [Project(project = json) for json in self.__saved_projects.find()]

    def get_project_by_name(self, name):
        for json in self._Database__saved_projects.find():
            if json["name"] == name:
                return Project(project = json)

        return None

    # Finds the project by name to delete
    def delete_project(self, project):
        self.__saved_projects.delete_one( { "name" : project.get_name() })

    # When adding the project, enforces a unique name
    def add_project(self, project):
        if self.__saved_projects.count_documents({"name" : project.get_name()}) > 0:
            raise Exception("Duplicate project name, " + project.get_name())
        self.__saved_projects.insert_one(project.get_json())

    # Update a project by passing in the old and new project
    def update_project(self, project):
        self.delete_project(project)
        self.add_project(project)

# Test Cases that make sure the database can store the projects as the
# app updates, adds and removes projects

class TestAddProject(unittest.TestCase):
    def setUp(self):
        self.database = Database.get_instance();
        self.project = Project(name = "Yodo", deadline = 4, description = "bashi", members = ["barribob", "power"])

    def test_add_project(self):
        num_projects = len(self.database.get_projects())
        self.database.add_project(self.project)
        self.assertEqual(len(self.database.get_projects()), num_projects + 1)
        self.database.delete_project(self.project)
        self.assertEqual(len(self.database.get_projects()), num_projects)

class TestUpdateProject(unittest.TestCase):
    def setUp(self):
        self.database = Database.get_instance();
        self.project = Project(name = "Yodo", deadline = 4, description = "bashi", members = ["barribob", "power"])
        self.task = Task(name = "Task1", deadline = 4, description = "desc", members = [])

    def test_update(self):
        self.database.add_project(self.project)
        self.project.add_task(self.task)
        self.database.update_project(self.project)
        tasks = len(self.database.get_project_by_name(self.project.get_name()).get_tasks())
        self.assertEqual(tasks, 1)
        self.database.delete_project(self.project)

if __name__ == "__main__":
    unittest.main()