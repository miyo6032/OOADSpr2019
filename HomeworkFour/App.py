#
# Homework 6 Final Project 
# Michael Yoshimura
# Gayathri Gude
#

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

    def get_name(self):
        return self.__name

    def get_deadline(self):
        return self.__deadline

    def get_description(self):
        return self.__description

    def get_members(self):
        return self.__members

    # Transforms the task into json to put into the database
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

# Responsible for managing all of the project through the database
class Database():
    __instance = None

    def __init__(self):
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
    def delete_project_by_name(self, project_name):
        self.__saved_projects.delete_one( { "name" : project_name })

    # When adding the project, enforces a unique name
    def add_project(self, project):
        if self.__saved_projects.count_documents({"name" : project.get_name()}) > 0:
            raise Exception("Duplicate project name, " + project.get_name())
        self.__saved_projects.insert_one(project.get_json())

    # Update a project by passing in the old and new project
    def update_project(self, project):
        self.delete_project_by_name(project.get_name())
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
        entry = tk.Entry(self, textvariable = StringVar(None))
        entry.pack(side="top", fill="x", expand=True)
        return entry

    def generate_button(self, parent, text, command):
        button = tk.Button(parent, text=text, command=command)
        button.pack(fill="both")
        return button

    def generate_frame(self, parent):
        return tk.LabelFrame(parent, pady = 0) 

    # "Hides" the frame by destroying it
    def hide(self):
        self.pack_forget()
        self.destroy() 

#
# Represents the page where the user creates a new project
#
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
        buttonsFrame = self.generate_frame(self)
        buttonsFrame.pack(side="bottom", fill="x")

        self.generate_button(buttonsFrame, "Save Project", self.saveProject).pack(side="left")
        self.generate_button(buttonsFrame, "Cancel", self.ui_facade.show_main_page).pack(side="right")

    # Saves project to the database, and returns back to the main page
    def saveProject(self): 
        title = self.titleField.get()  
        description = self.descriptionField.get() 
        deadline = self.deadlineField.get() 
        team = self.teamField.get() 

        newProject = Project(title, description, deadline, team) 
        Database.get_instance().add_project(newProject) 

        self.ui_facade.show_main_page()

#
# Represents the main page that shows all of the different projects
#
class PageMain(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

    # Where all of the page element generation happens
    # Basically loads the page
    def generate_page(self):
        database = Database.get_instance()

        # Generate title
        self.generate_title(self, "Project")

        self.__buttonframe = self.generate_frame(self)
        self.__buttonframe.pack(side="top", fill="both", expand=False)

        # Generates all of the buttons for each project from the database
        for project in database.get_projects():
            self.generate_project(project.get_name())

        # Add Project button
        add_project_frame = self.generate_frame(self)
        add_project_frame.pack(side="bottom", fill="both")
        self.generate_button(add_project_frame, "Add Project", self.ui_facade.show_add_project).pack(side="left")

    # Creates a new project entry with the view and delete buttons
    def generate_project(self, project_name):
        project_frame = self.generate_frame(self)
        project_frame.pack(side="top", fill="x")

        self.generate_label(project_frame, project_name).pack(side="left", fill="x", expand=True)

        self.generate_button(project_frame, "Delete", lambda : self.show_confirm_delete(project_name)).pack(side="right", fill="both")
        
        project = Database.get_instance().get_project_by_name(project_name)
        self.generate_button(project_frame, "View", lambda : self.ui_facade.showProjectDetails(project)).pack(side="right", fill="both")

    # Shows a dialogue for confirming the deletion of a project
    def show_confirm_delete(self, project_name):
        confirm_delete_window = tk.Toplevel()
        confirm_delete_window.wm_title("Delete Project?")

        self.generate_label(confirm_delete_window, "Delete Project " + project_name + "?").pack(side="top")

        options_frame = self.generate_frame(confirm_delete_window)
        options_frame.pack(side="bottom", fill="both")

        # Yes and no buttons
        self.generate_button(options_frame, "Yes, Delete", lambda : self.delete_project(project_name, confirm_delete_window)).pack(side="left")
        self.generate_button(options_frame, "Cancel", confirm_delete_window.destroy).pack(side="right")
        
        # Makes this window the only interactable window
        confirm_delete_window.grab_set()

    # Delete the project from the database, updates the window, and closes the delete confirm window
    def delete_project(self, project_name, popup_window):
        Database.get_instance().delete_project_by_name(project_name)
        self.ui_facade.show_main_page()
        popup_window.grab_release()
        popup_window.destroy()

#
# Represents the project page, where a specific project is shown
#
class ProjectDescription(Page): 
    def __init__(self, ui_facade, project, *args, **kwargs):
        self.project = project
        Page.__init__(self, ui_facade, *args, **kwargs)

    def generate_page(self):
        self.generate_title(self, self.project.get_name())

        # Frames for organizing the page
        detailsFrame = self.generate_frame(self)
        detailsFrame.pack(side="left", fill="both")

        self.tasksFrame = self.generate_frame(self)
        self.tasksFrame.pack(side="left", fill="both", expand=True) 

        for task in self.project.get_tasks():
            self.generate_task(task)

        # Generate the project details on the side
        self.generate_label(detailsFrame, self.project.get_projectDetails())
        self.generate_label(detailsFrame, self.project.get_deadline())
        self.generate_label(detailsFrame, self.project.get_members())

        # Generates the buttons at the bottom
        miniFrame = self.generate_frame(self.tasksFrame)
        miniFrame.pack(side="bottom", fill="both")

        self.generate_button(miniFrame, "Main Menu", self.ui_facade.show_main_page).pack(side="right", fill="both")
        self.generate_button(miniFrame, "Add Tasks", lambda : self.ui_facade.showAddTask(self.project)).pack(side="left", fill="both")

    # Represents one task in the list of tasks for the page
    def generate_task(self, task):
        task_frame = self.generate_frame(self.tasksFrame)
        task_frame.pack(side="top", fill="x")

        self.generate_label(task_frame, task.get_name()).pack(side="left", fill="x", expand=True)

        self.generate_button(task_frame, "Delete", lambda : self.show_confirm_delete(task)).pack(side="right")
        self.generate_button(task_frame, "View", lambda : self.ui_facade.showTask(self.project, task)).pack(side="right")

    # Creates a new project entry with the view and delete buttons
    def create_project(self, project_name):
        project_frame = self.generate_frame(self)
        project_frame.pack(side="top", fill="x")

        self.generate_label(project_frame, project_name).pack(side="left", fill="x", expand=True)

        self.generate_button(project_frame, "Delete", lambda : self.show_confirm_delete(project_name)).pack(side="right", fill="both")
        
        project = Database.get_instance().get_project_by_name(project_name)
        self.generate_button(project_frame, "View", lambda : self.ui_facade.showProjectDetails(project)).pack(side="right", fill="both")

    # Shows a dialogue for confirming the deletion of a project
    def show_confirm_delete(self, task):
        confirm_delete_window = tk.Toplevel()
        confirm_delete_window.wm_title("Delete Task?")

        self.generate_label(confirm_delete_window, "Delete Task " + task.get_name() + "?").pack(side="top")

        options_frame = self.generate_frame(confirm_delete_window)
        options_frame.pack(side="bottom", fill="both")

        # Yes and no buttons
        self.generate_button(options_frame, "Yes, Delete", lambda : self.delete_task(task, confirm_delete_window)).pack(side="left")
        self.generate_button(options_frame, "Cancel", confirm_delete_window.destroy).pack(side="right")
        
        # This window is the only interactable window
        confirm_delete_window.grab_set()

    # Delete the project from the database, updates the window, and closes the delete confirm window
    def delete_task(self, task, popup_window):
        self.project.remove_task(task)
        Database.get_instance().update_project(self.project)
        self.ui_facade.showProjectDetails(self.project)
        popup_window.grab_release()
        popup_window.destroy()

#
# Represents the page where the user creates a new task for a certain project
#
class PageAddTask(Page):
    def __init__(self, ui_facade, project, *args, **kwargs):
        self.project = project
        Page.__init__(self, ui_facade, *args, **kwargs)

    def generate_page(self):
        self.generate_title(self, "New Task")

        # Labels and input fields for a new task
        self.generate_label(self, "Task Title")
        self.titleField = self.generate_entry(self)
        self.generate_label(self, "Task Description")
        self.descriptionField = self.generate_entry(self)
        self.generate_label(self, "Task Deadline")
        self.deadlineField= self.generate_entry(self)
        self.generate_label(self, "Associated Members")
        self.members = self.generate_entry(self)

        # For the buttons 
        buttonsFrame = self.generate_frame(self)
        buttonsFrame.pack(side="bottom", fill="x")

        self.generate_button(buttonsFrame, "Add Task", self.saveTask).pack(side="left")
        self.generate_button(buttonsFrame, "Cancel", lambda : self.ui_facade.showProjectDetails(self.project)).pack(side="right")

    # Saves task to the database, and returns back to the project page
    def saveTask(self): 
        title = self.titleField.get()  
        description = self.descriptionField.get() 
        deadline = self.deadlineField.get() 
        members = self.members.get().split()

        self.project.add_task(Task(name=title, description=description, deadline=deadline, members=members))
        Database.get_instance().update_project(self.project)

        self.ui_facade.showProjectDetails(self.project)

#
# Simple task view page
#
class ViewTask(Page):
    def __init__(self, ui_facade, task, project, *args, **kwargs):
        self.task = task
        self.project = project
        Page.__init__(self, ui_facade, *args, **kwargs)

    def generate_page(self):
        self.generate_title(self, self.task.get_name())

        self.generate_label(self, self.task.get_description())
        self.generate_label(self, self.task.get_deadline())
        self.generate_label(self, self.task.get_members())

        button_frame = self.generate_frame(self)
        button_frame.pack(side="bottom", fill="x")

        self.generate_button(button_frame, "Back to Project", lambda : self.ui_facade.showProjectDetails(self.project))

#
# Responsible for mediating page changes
#
# Basically works by destroying the page that is not needed
# and instantiating the new page. This method is not super
# efficient, but for our purposes, it simplifies a lot of operations
# and makes it so that we do not need to mediate messages using the
# observer pattern
#
class UIFacade(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.current_page = PageMain(self)

        # This is the frame that contains each page required
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.show_page(PageMain(self))

    # Place the page into the ui_facade container
    def show_page(self, page):
        self.current_page.hide()
        page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)  

    #
    # The functions below are responsible for changing the app to the correct page requested
    #
    def show_main_page(self): 
        self.show_page(PageMain(self)) 

    def show_add_project(self):
        self.show_page(PageAddProject(self)) 

    def showProjectDetails(self, project): 
        self.show_page(ProjectDescription(self, project))

    def showAddTask(self, project): 
        self.show_page(PageAddTask(self, project))

    def showTask(self, project, task):
        self.show_page(ViewTask(self, task, project))

# The main app just encapulates some of the weirdness in instantiating the UI components
class App():
    def main(self, windowX, windowY):
        root = tk.Tk()
        main = UIFacade(root)
        main.pack(side="top", fill="both", expand=True)
        root.wm_geometry(str(windowX) + "x" + str(windowY))
        root.mainloop()  

if __name__ == "__main__":
    App().main(600, 600)