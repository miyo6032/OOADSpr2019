import pymongo as pm
import tkinter as tk
from tkinter import StringVar, Label, Entry

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
        for json in self.__saved_projects.find():
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

#
# Begin UI and Front End Elements
#

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()

    def hide(self):
        pass

class PageAddProject(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        t = tk.Toplevel(self)
        t.wm_title("New Project")
        l = tk.Label(t, text="NEW PROJECT")
        l.pack(side="top", fill="both", expand=True) 


        label = tk.Label(self, text="Project Name")
        
        # label_input = tk.Label(self, text="Search")
        # e = tk.Entry(t)
        # #e.insert(0, "a default value")
        # e.pack(side="top", fill="both", padx=100)
        # # e.grid(row=0, column=1)

        labelText=StringVar()
        labelText.set("Project Title")
        labelDir=Label(t, textvariable=labelText, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        directory=StringVar(None)
        dirname=Entry(t,textvariable=directory,width=50)
        dirname.pack(side="top", fill="both", expand=True) 

        #namebox.insert(END, names + '\n')
        
        labelText=StringVar()
        labelText.set("Project Description")
        labelDir=Label(t, textvariable=labelText, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        directory=StringVar(None)
        dirname=Entry(t,textvariable=directory,width=50)
        dirname.pack(side="top", fill="both", expand=True)

        labelText=StringVar()
        labelText.set("Project Deadline")
        labelDir=Label(t, textvariable=labelText, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        directory=StringVar(None)
        dirname=Entry(t,textvariable=directory,width=50)
        dirname.pack(side="top", fill="both", expand=True)

        labelText=StringVar()
        labelText.set("Project Team Members")
        labelDir=Label(t, textvariable=labelText, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        directory=StringVar(None)
        dirname=Entry(t,textvariable=directory,width=50)
        dirname.pack(side="top", fill="both", expand=True) 
    
class PageMain(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.update()

    def update(self):
        database = Database.get_instance();

        if(hasattr(self, '__buttonframe')):
            self.__buttonframe.destroy();

        self.__buttonframe = tk.Frame(self)
        self.__buttonframe.pack(side="top", fill="both", expand=False)

        # Generates all of the buttons for each project from the database
        for project in database.get_projects():
            self.create_project(project.get_name())

        b4 = tk.Button(self.__buttonframe, text="Add Project")
        b4.pack(side="bottom")

    # Creates a new project button
    def create_project(self, project_name):
        new_project = tk.Button(self.__buttonframe, text=project_name) 
        new_project.pack(side="top", fill="both", expand=True)

class UIFacade(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = PageMain(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Projects", command=p1.lift)

        b1.pack(side="left")
        
        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    main = UIFacade(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()