import pymongo as pm
import tkinter as tk
from tkinter import StringVar, Label, Entry
from abc import ABC, abstractmethod

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

    def get_deadline(self): 
        return self.__deadline 
    
    def get_members(self): 
        return self.__members 

    def get_projectDetails(self): 
        return self.__description

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
    def delete_project(self, project_name):
        self.__saved_projects.delete_one( { "name" : project_name })

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

# The multiple inheritance is required because the page needs to be
# abstract and a tkinter Frame.
class Page(tk.Frame, ABC):
    def __init__(self, ui_facade, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.ui_facade = ui_facade
        # Some constants to maintain consistency between pages
        self.title_font_size = 20

        self.generate_page()

    @abstractmethod
    def generate_page(self):
        pass

    def generate_label(self, parent, text):
        label = tk.Label(parent, text=text, anchor='w')
        label.pack(side="top", fill="both")
        return label

    def generate_title(self, parent, text):
        title = tk.Label(parent, text = text, anchor='w', font=("Arial", self.title_font_size))
        title.pack(fill='both')
        return title

    def generate_entry(self, parent):
        entry = tk.Entry(self,textvariable = StringVar(None))
        entry.pack(side="top", fill="x", expand=True)
        return entry

    # "Hides" the frame by destroying it
    def hide(self):
        self.pack_forget()
        self.destroy() 

class PageAddProject(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    def generate_page(self):
        self.generate_title(self, "New Project")

        self.generate_label(self, "Project Title")
        self.titleField = self.generate_entry(self)
        self.generate_label(self, "Project Description")
        self.descriptionField = self.generate_entry(self)
        self.generate_label(self, "Project Deadline")
        self.deadlineField= self.generate_entry(self)
        self.generate_label(self, "Project Team Members")
        self.teamField = self.generate_entry(self)

        # For the buttons 
        buttonsFrame = tk.Frame(self)
        buttonsFrame.pack(side="bottom", fill="x")

        tk.Button(buttonsFrame, text="Save Project", command=self.saveProject) .pack(side="left")
        tk.Button(buttonsFrame, text="Cancel", command=self.ui_facade.show_main_page).pack(side="right")

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

    # Where all of the page element generation happens
    # Basically loads the page
    def generate_page(self):
        database = Database.get_instance()

        # Generate title
        self.generate_title(self, "Project")

        if(hasattr(self, '__buttonframe')):
            self.__buttonframe.destroy();

        self.__buttonframe = tk.Frame(self)
        self.__buttonframe.pack(side="top", fill="both", expand=False)

        # Generates all of the buttons for each project from the database
        for project in database.get_projects():
            self.create_project(project.get_name())

        # Add Project button
        add_project_frame = tk.Frame(self)
        add_project_frame.pack(side="bottom", fill="both")
        add_project_button = tk.Button(add_project_frame, text="Add Project", command=self.ui_facade.show_add_project)
        add_project_button.pack(side="left")

    # Creates a new project entry with the view and delete buttons
    def create_project(self, project_name):
        project_frame = tk.Frame(self.__buttonframe, borderwidth = 1, background="gray")
        project_frame.pack(side="top", fill="both", expand=True)
        
        project_title = tk.Label(project_frame, text=project_name, anchor='w')
        project_title.pack(side="left", fill="both", expand=True)

        delete_project_button = tk.Button(project_frame, text="Delete", command=lambda : self.show_confirm_delete(project_name))
        delete_project_button.pack(side="right", fill="both")
         
        project = Database.get_instance().get_project_by_name(project_name)
        view_project_button = tk.Button(project_frame, text="View", command=lambda : self.ui_facade.showProjectDetails(project))
        view_project_button.pack(side="right", fill="both")

    # Shows a dialogue for confirming the deletion of a project
    def show_confirm_delete(self, project_name):
        confirm_delete_window = tk.Toplevel()
        confirm_delete_window.wm_title("Delete Project?")

        confirm_delete_text = tk.Label(confirm_delete_window, text="Delete Project " + project_name + "?")
        confirm_delete_text.pack(side="top")

        options_frame = tk.Frame(confirm_delete_window)
        options_frame.pack(side="bottom", fill="both")

        yes_button = tk.Button(options_frame, text="Yes, Delete", command=lambda : self.delete_project(project_name, confirm_delete_window))
        yes_button.pack(side="left")

        no_button = tk.Button(options_frame, text="Cancel", command=confirm_delete_window.destroy)
        no_button.pack(side="right")
        
        # This window is the only interactable window
        confirm_delete_window.grab_set()

    # Delete the project from the database, updates the window, and closes the delete confirm window
    def delete_project(self, project_name, popup_window):
        Database.get_instance().delete_project(project_name)
        self.ui_facade.show_main_page()
        popup_window.grab_release()
        popup_window.destroy()

class ProjectDescription(Page): 
    def __init__(self, ui_facade, project, *args, **kwargs):
        self.project = project
        Page.__init__(self, ui_facade, *args, **kwargs)
        #Database.get_instance

    def generate_page(self):
        #t = tk.Toplevel(self)
        #t.wm_title("Project Details")

        nameFrame = tk.LabelFrame(self, pady = 0)  
        nameFrame.pack(side="top", fill="both")

        detailsFrame = tk.LabelFrame(self, pady = 0) 
        detailsFrame.pack(side="left", fill="both")

        tasksFrame = tk.LabelFrame(self, pady=0) 
        tasksFrame.pack(side="left", fill="both") 

        miniFrame = tk.LabelFrame(tasksFrame, pady=0) 
        miniFrame.pack(side="bottom", fill="both")

        l = tk.Label(detailsFrame, text=self.project.get_projectDetails(), bg="white", fg="black", borderwidth=5, relief="groove")
        l.pack(side="top", fill="both", expand=True)
        label = tk.Label(self, text=self.project.get_name())

        projectTitle=StringVar()
        projectTitle.set(self.project.get_name())
        labelDir=Label(nameFrame, textvariable=projectTitle, height=4, bg="white", fg="black", borderwidth=5, relief="groove")
        labelDir.pack(side="top", fill="both", expand=True)

        projDeadline=StringVar()
        projDeadline.set(self.project.get_deadline())
        labelDir=Label(detailsFrame, textvariable=projDeadline, height=4, bg="white", fg="black", borderwidth=5, relief="groove")
        labelDir.pack(side="top", fill="both", expand=True)

        projDeadline=StringVar()
        projDeadline.set(self.project.get_members())
        labelDir=Label(detailsFrame, textvariable=projDeadline, height=4, bg="white", fg="black", borderwidth=5, relief="groove")
        labelDir.pack(side="top", fill="both", expand=True)

        addTasks = tk.Button(miniFrame, text="Main Menu", command=self.ui_facade.show_main_page)
        addTasks.pack(side="left", fill="both")

        addTasks = tk.Button(miniFrame, text="Add Tasks")
        addTasks.pack(side="right", fill="both")
        

class UIFacade(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.add_project_page = None
        self.main_page = PageMain(self)
        self.projectDetails = None 
        self.pages = [self.add_project_page, self.main_page, self.projectDetails]

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        # Place the main page
        self.show_page(self.main_page)

    # Place the page into the ui_facade container
    def show_page(self, page):
        page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)  
    
    def close_all_pages(self):
        for page in self.pages:
            if(page != None):
                page.hide()

    def show_main_page(self): 
        self.close_all_pages()
        self.main_page = PageMain(self) 
        self.show_page(self.main_page) 

    # Hides all pages before opening the page to add projects
    def show_add_project(self):
        self.close_all_pages()

        # To make the page show, instantiate the page first
        self.add_project_page = PageAddProject(self)
        self.show_page(self.add_project_page) 

    def showProjectDetails(self, project): 
        self.close_all_pages() 
        self.projectDetails = ProjectDescription(self, project) 
        self.show_page(self.projectDetails)

if __name__ == "__main__":
    root = tk.Tk()
    main = UIFacade(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("400x400")
    root.mainloop()