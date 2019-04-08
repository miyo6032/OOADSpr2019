import pymongo as pm

# Responsible for holding task data
class Task:
    def __init__(self, name = "", deadline = 0, description = "", members = [], task = None):
        if task == None:
            self.__name = name
            self.__deadline = deadline
            self.__description = description
            self.__team_members = members
        else:
            self.__name = task["name"]
            self.__deadline = task["deadline"]
            self.__description = task["description"]
            self.__team_members = task["members"]

    def get_json(self):
        return {"name": self.__name, "deadline": self.__deadline, "description": self.__description, "members": self.__members}

    def __str__(self):
        return self.get_json().__str__()

    def __repr__(self):
        return self.__str__()

# Responsible for keeping track of its tasks
class Project:
    def __init__(self, name = "", deadline = 0, description = "", members = [], project = None):
        if project == None:
            self.__tasks = []
            self.__name = name
            self.__deadline = deadline
            self.__description = description
            self.__members = members
        else:
            self.__tasks = project["tasks"]
            self.__name = project["name"]
            self.__deadline = project["deadline"]
            self.__description = project["description"]
            self.__members = project["members"]

    def add_task(self, task):
        self.__tasks.append(task)

    def remove_task(self, task):
        self.__tasks.remove(task)

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

    def delete_project(self, project):
        self.__saved_projects.delete_one(project.get_json())

    def add_project(self, project):
        self.__saved_projects.insert_one(project.get_json())

    # Update a project by passing in the project and a dictionary key value for which values to update
    def update_project(self, project, update):
        self.__saved_projects.update_one(project.get_json(), { "$set": update })

if __name__ == "__main__":
    d = Database.get_instance();
    p = Project(name = "Yodo", deadline = 4, description = "bashi", members = ["barribob", "power"])
    d.add_project(p);
    # d.delete_project(p);

    for p in d.get_projects():
        print(p)

    for p in d.get_projects():
        d.update_project(p, {"name": "Yolo"})

    for p in d.get_projects():
        print(p)