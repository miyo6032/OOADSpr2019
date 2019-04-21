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
    def __init__(self, ui_facade, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.ui_facade = ui_facade

    # "Hides" the frame by destroying it
    def hide(self):
        self.pack_forget()
        self.destroy() 

class PageAddProject(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        t = self
        l = tk.Label(t, text="NEW PROJECT")
        l.pack(side="top", fill="both", expand=True) 

        title=StringVar()
        title.set("Project Title")
        labelDir=Label(t, textvariable=title, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        inputTitle=StringVar(None)
        self.titleField=Entry(t,textvariable=inputTitle,width=50)
        self.titleField.pack(side="top", fill="both", expand=True) 

        #namebox.insert(END, names + '\n')
        
        description=StringVar()
        description.set("Project Description")
        labelDir=Label(t, textvariable=description, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        inputDescription=StringVar(None)
        self.descriptionField=Entry(t,textvariable=inputDescription,width=50)
        self.descriptionField.pack(side="top", fill="both", expand=True)

        deadline=StringVar()
        deadline.set("Project Deadline")
        labelDir=Label(t, textvariable=deadline, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        deadlineInput=StringVar(None)
        self.deadlineField=Entry(t,textvariable=deadlineInput,width=50)
        self.deadlineField.pack(side="top", fill="both", expand=True)

        team=StringVar()
        team.set("Project Team Members")
        labelDir=Label(t, textvariable=team, height=4)
        labelDir.pack(side="top", fill="both", expand=True)

        teamInput=StringVar(None)
        self.teamField=Entry(t,textvariable=teamInput,width=50)
        self.teamField.pack(side="top", fill="both", expand=True)  

        saveButton = tk.Button(text="Save Project", command=self.saveProject) 
        saveButton.pack(side="bottom")

    # Saves project to the database, and returns back to the main page
    def saveProject(self): 
        title = self.titleField.get()  
        description = self.descriptionField.get() 
        deadline = self.deadlineField.get() 
        team = self.teamField.get() 

        newProject = Project(title, description, deadline, team) 
        Database.get_instance().add_project(newProject) 

        self.ui_facade.show_main_page()

class PageMain(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        self.update()

    # Where all of the page element generation happens
    # Basically loads the page
    def update(self):
        database = Database.get_instance();

        if(hasattr(self, '__buttonframe')):
            self.__buttonframe.destroy();

        self.__buttonframe = tk.Frame(self)
        self.__buttonframe.pack(side="top", fill="both", expand=False)

        # Generates all of the buttons for each project from the database
        for project in database.get_projects():
            self.create_project(project.get_name())

        # This button links to the show add project page
        add_project_button = tk.Button(self.__buttonframe, text="Add Project", command=self.ui_facade.show_add_project)
        add_project_button.pack(side="bottom")

        projects = tk.Button(self, text="Projects")
        projects.pack(side="left")

    # Creates a new project button
    def create_project(self, project_name):
        new_project = tk.Button(self.__buttonframe, text=project_name) 
        new_project.pack(side="top", fill="both", expand=True)

class UIFacade(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.add_project_page = None
        self.main_page = PageMain(self)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Place the main page
        self.show_page(self.main_page)
        
    # Hides the main page before opening the page to add projects
    def show_add_project(self):
        self.main_page.hide()

        # To make the page show, instantiate the page first
        self.add_project_page = PageAddProject(self)
        self.show_page(self.add_project_page)

    # Place the page into the ui_facade container
    def show_page(self, page):
        page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)  
    
    def show_main_page(self): 
        self.add_project_page.hide  
        self.main_page = PageMain(self) 
        self.show_page(self.main_page) 

if __name__ == "__main__":
    root = tk.Tk()
    main = UIFacade(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()