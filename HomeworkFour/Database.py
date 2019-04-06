class Task:
    def __init__(self, name, deadline, description, members):
        self.__name = name
        self.__deadline = deadline
        self.__description = description
        self.__team_members = members

    def __str__(self):
        return "Task " + self.__name

    def __repr__(self):
        return self.__str__()

class Project:
    def __init__(self, name, deadline, description, members):
        self.__tasks = []
        self.__name = name
        self.__deadline = deadline
        self.__description = description
        self.__team_members = members

    def add_task(self, task):
        self.__tasks.append(task)

    def remove_task(self, task):
        self.__tasks.remove(task)

    def __str__(self):
        return "Project " + self.__name

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

class Database(Subject):
    __instance = None

    def __init__(self):
        Subject.__init__(self)
        if Database.__instance != None: # Prevents more than one instance of the singleton from occurring
            raise Exception("Attempt to more than one Database singleton instance.")
        
        Database.__instance = self
        self.__projects = []

    @staticmethod
    def get_instance(): # Can be accessed anywhere to get the instance of database
        if Database.__instance == None:
            Database() # Call the constructor it instantiate an instance
        return Database.__instance

    def get_projects(self):
        return self.__projects

    def delete_project(self, project):
        self.__projects.remove(project)

    def add_project(self, project):
        self.__projects.append(project)

    def load():
        pass

    def save():
        pass 

if __name__ == "__main__":
    database = Database.get_instance()
    p = Project("yodo", 4, "bashi", "barribob")
    t = Task("yodo", 4, "bashi", "barribob")